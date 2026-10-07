from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.config import PROCESSED_DATA, MODEL_DIR
from app.components.model_ui import employment_form

from app.components.ui_config import apply_2026_theme
apply_2026_theme(page_title="Employment Prediction", page_icon="🔮")



st.title("🔮 Predictive Employment Engine")
st.markdown("Use the form below to input a graduate's profile. The machine learning model will calculate the exact probability of this candidate securing employment based on historical trends.")

df = pd.read_csv(PROCESSED_DATA)

with st.container(border=True):
    st.subheader("📝 Candidate Profile Input")
    inputs = employment_form(df)
    
st.divider()

if st.button("🚀 Calculate Employment Probability", type="primary", use_container_width=True):
    with st.spinner("Analyzing candidate profile..."):
        # Call R script instead of Python model!
        import subprocess
        import json
        import platform
        
        # Cross-platform Rscript path
        if platform.system() == "Windows":
            RSCRIPT_PATH = r"E:\R-4.6.1\bin\Rscript.exe"
        else:
            RSCRIPT_PATH = "Rscript"
        
        script_path = str(Path(__file__).resolve().parents[2] / "R" / "predict_new.R")
        
        inputs_json = inputs.to_json(orient='records')
        
        try:
            result = subprocess.run(
                [RSCRIPT_PATH, script_path, inputs_json], 
                capture_output=True, text=True, check=True
            )
            
            # The R script prints JSON to standard output. 
            # We look for the last line which contains the JSON.
            lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            r_output = json.loads(lines[-1])
            emp_prob = r_output["employed_probability"]
            not_emp_prob = 1.0 - emp_prob
            probability = [not_emp_prob, emp_prob]
        except FileNotFoundError:
            st.error(f"⚠️ **Could not find Rscript!** Python cannot find the R executable.")
            st.warning(f"**How to fix:** Open `04_Employment_Prediction.py` (around line 34) and change `RSCRIPT_PATH` to the exact path where R is installed on your computer. For example: `r\"C:\\Program Files\\R\\R-4.4.1\\bin\\Rscript.exe\"`")
            st.stop()
        except subprocess.CalledProcessError as e:
            st.error(f"Error connecting to R backend: {e}")
            st.error(f"R Output: {e.stderr}")
            st.stop()
        except Exception as e:
            st.error(f"Error connecting to R backend: {e}")
            st.stop()
        
        st.markdown("### 🎯 Prediction Results")
        st.markdown("<hr style='margin-top: 0; margin-bottom: 2rem;'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            if emp_prob >= 0.5:
                st.success(f"### 🎉 Likely Employed")
                st.markdown("Based on historical data and the provided attributes, this candidate has a strong profile and is projected to secure employment.")
            else:
                st.error(f"### ⚠️ At Risk")
                st.markdown("This candidate's profile indicates a higher likelihood of remaining unemployed or continuing education. Targeted interventions may be recommended.")
                
        with col2:
            import plotly.graph_objects as go
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = emp_prob * 100,
                title = {'text': "Employment Probability", 'font': {'size': 24, 'color': '#1E3A8A'}},
                number = {'suffix': "%", 'font': {'size': 40, 'color': '#1E3A8A'}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "#2563EB" if emp_prob >= 0.5 else "#EF4444"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 50], 'color': '#FEE2E2'},
                        {'range': [50, 100], 'color': '#DCFCE7'}],
                }
            ))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=300, margin=dict(l=10, r=10, t=50, b=10))
            st.plotly_chart(fig, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.warning("⚠️ **Disclaimer:** This is a model-based estimate generated from historical associations. It should not be used as an absolute individual employability label.")
