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

@st.cache_data
def load_data():
    return pd.read_csv(PROCESSED_DATA)

df = load_data()

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
        
        # Cross-platform Rscript path with automatic fallback
        if platform.system() == "Windows":
            default_path = r"E:\R-4.6.1\bin\Rscript.exe"
            import shutil
            RSCRIPT_PATH = default_path if Path(default_path).exists() else (shutil.which("Rscript") or "Rscript")
        else:
            RSCRIPT_PATH = "Rscript"
        
        script_path = str(Path(__file__).resolve().parents[2] / "R" / "predict_new.R")
        
        inputs_json = inputs.to_json(orient='records')
        
        try:
            root_dir = str(Path(__file__).resolve().parents[2])
            result = subprocess.run(
                [RSCRIPT_PATH, script_path, inputs_json], 
                capture_output=True, text=True, check=True,
                cwd=root_dir
            )
            
            # The R script prints JSON to standard output. 
            lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            if not lines:
                st.error("⚠️ **R Backend returned empty output.**")
                if result.stderr:
                    st.code(result.stderr, language="text")
                st.stop()
            
            try:
                r_output = json.loads(lines[-1])
            except json.JSONDecodeError:
                st.error("⚠️ **Could not parse response from R backend:**")
                st.code(result.stdout, language="text")
                if result.stderr:
                    st.code(result.stderr, language="text")
                st.stop()
            
            raw_prob = r_output.get("employed_probability", 0.5)
            if isinstance(raw_prob, dict):
                values = list(raw_prob.values())
                emp_prob = float(raw_prob.get("Employed", values[0] if values else 0.5))
            elif raw_prob is not None:
                emp_prob = float(raw_prob)
            else:
                emp_prob = 0.5
                
            raw_salary = r_output.get("predicted_salary", None)
            if isinstance(raw_salary, dict):
                values = list(raw_salary.values())
                predicted_salary = float(values[0]) if values else None
            elif raw_salary is not None:
                predicted_salary = float(raw_salary)
            else:
                predicted_salary = None
                
            not_emp_prob = 1.0 - emp_prob
            probability = [not_emp_prob, emp_prob]
        except FileNotFoundError:
            st.error(f"⚠️ **Could not find Rscript!** Python cannot find the R executable.")
            st.warning(f"**How to fix:** Please ensure R is installed and configured in your environment PATH.")
            st.stop()
        except subprocess.CalledProcessError as e:
            st.error(f"Error connecting to R backend: {e}")
            if e.stderr:
                st.error(f"R Output: {e.stderr}")
            st.stop()
        except Exception as e:
            st.error(f"Error connecting to R backend: {e}")
            st.stop()
        
        st.markdown("### 🎯 Prediction Results")
        st.markdown("<hr style='margin-top: 0; margin-bottom: 2rem;'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.markdown("<br>", unsafe_allow_html=True)
            if emp_prob >= 0.5:
                st.success(f"### 🎉 Positive Classification (Employed)")
                if predicted_salary is not None:
                    st.metric("Estimated Starting Salary (Linear Regression)", f"${predicted_salary:,.2f}")
                st.markdown(
                    "**Statistical Inference:** The candidate is classified as **Employed** "
                    "with a predicted probability exceeding the 50% decision threshold.\n\n"
                    "**Model Architecture:**\n"
                    "- **Employment Status:** Evaluated using **Random Forest** (decision tree ensemble), modeling interactions between degree level, university ranking, GPA, and internships.\n"
                    "- **Starting Salary:** Projected using **Multiple Linear Regression**, benchmarked on historical graduate compensation data."
                )
            else:
                st.error(f"### ⚠️ Negative Classification (Unemployed/Other)")
                if predicted_salary is not None:
                    st.metric("Estimated Potential Salary Upon Placement (Linear Regression)", f"${predicted_salary:,.2f}")
                st.markdown(
                    "**Statistical Inference:** The candidate is classified as **Unemployed/Other** "
                    "as the predicted probability falls below the 50% decision threshold.\n\n"
                    "**Model Architecture:**\n"
                    "- **Employment Status:** Evaluated using **Random Forest** (decision tree ensemble) based on academic profile and employment trends.\n"
                    "- **Potential Salary:** Projected benchmark salary calculated using **Multiple Linear Regression** upon successful job placement."
                )
                
        with col2:
            import plotly.graph_objects as go
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = emp_prob * 100,
                title = {'text': "Employment Probability", 'font': {'size': 20, 'color': '#f8fafc'}},
                number = {'suffix': "%", 'font': {'size': 38, 'color': '#f8fafc'}},
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
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=280, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.warning("⚠️ **Disclaimer:** This is a model-based estimate generated from historical associations. It should not be used as an absolute individual employability label.")
