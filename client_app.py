from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import base64
import subprocess
import json
import platform

# Root configuration
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.config import PROCESSED_DATA
from app.components.model_ui import employment_form

from app.components.ui_config import apply_2026_theme

# Apply the main project theme to get all the nice glassmorphism and fonts
apply_2026_theme(page_title="Employment Prediction Portal", page_icon="🔮")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_dark_background(png_file):
    try:
        bin_str = get_base64_of_bin_file(png_file)
        # We add a dark linear gradient overlay over the image so white text is highly readable
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: 
                linear-gradient(to bottom, rgba(2, 6, 23, 0.8), rgba(2, 6, 23, 0.9)),
                url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except Exception as e:
        pass

# Apply the professional background image with dark overlay
bg_path = ROOT / "res" / "background.jpg"
if bg_path.exists():
    set_dark_background(bg_path)

st.markdown("<h1 style='text-align: center;'>🎓 Graduate Employment Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em; color: #cbd5e1;'>Welcome to our advanced predictive engine. Evaluate candidate profiles to forecast employment outcomes.</p>", unsafe_allow_html=True)
st.markdown("---")

df = pd.read_csv(PROCESSED_DATA)

with st.container():
    st.subheader("📝 Candidate Profile Input")
    inputs = employment_form(df)
    
st.divider()

if st.button("🚀 Calculate Employment Probability", type="primary", use_container_width=True):
    with st.spinner("Analyzing candidate profile against historical data..."):
        # Cross-platform Rscript path
        if platform.system() == "Windows":
            RSCRIPT_PATH = r"E:\R-4.6.1\bin\Rscript.exe"
        else:
            RSCRIPT_PATH = "Rscript"
        
        script_path = str(ROOT / "R" / "predict_new.R")
        inputs_json = inputs.to_json(orient='records')
        
        try:
            result = subprocess.run(
                [RSCRIPT_PATH, script_path, inputs_json], 
                capture_output=True, text=True, check=True
            )
            
            lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            r_output = json.loads(lines[-1])
            emp_prob = r_output["employed_probability"]
        except FileNotFoundError:
            st.error("⚠️ **Could not find Rscript!** Please configure the correct path in `client_app.py`.")
            st.stop()
        except subprocess.CalledProcessError as e:
            st.error(f"Error connecting to R backend: {e}")
            st.stop()
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            st.stop()
        
        st.markdown("### 🎯 Prediction Results")
        st.markdown("<hr style='margin-top: 0; margin-bottom: 2rem;'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            if emp_prob >= 0.5:
                st.success(f"### 🎉 Highly Competitive Candidate")
                st.markdown(
                    "**Assessment:** This candidate demonstrates a highly attractive profile for the current job market.\n\n"
                    "**Market Insights:** Candidates with this combination of education, GPA, and background typically "
                    "transition smoothly into full-time roles. Their profile aligns strongly with current employer demands. "
                    "We recommend fast-tracking this candidate through the hiring pipeline or recruitment process."
                )
            else:
                st.error(f"### ⚠️ Needs Targeted Support")
                st.markdown(
                    "**Assessment:** This candidate may face friction entering the primary job market based on current industry trends.\n\n"
                    "**Market Insights:** Market data suggests candidates with similar profiles often benefit from targeted upskilling, "
                    "internships, or bridge programs before securing a permanent role. We recommend offering them career counseling, "
                    "resume workshops, or directing them toward specialized entry-level pipelines."
                )
                
        with col2:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = emp_prob * 100,
                title = {'text': "Employment Probability", 'font': {'size': 20, 'color': '#f8fafc'}},
                number = {'suffix': "%", 'font': {'size': 36, 'color': '#f8fafc'}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#8b5cf6" if emp_prob >= 0.5 else "#f43f5e"},
                    'bgcolor': "rgba(30, 41, 59, 0.5)",
                    'borderwidth': 2,
                    'bordercolor': "rgba(255,255,255,0.1)",
                    'steps': [
                        {'range': [0, 50], 'color': 'rgba(244, 63, 94, 0.2)'},
                        {'range': [50, 100], 'color': 'rgba(139, 92, 246, 0.2)'}],
                }
            ))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=250, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.info("⚠️ **Disclaimer:** This is a model-based estimate generated from historical associations. It should not be used as an absolute individual employability label.")
