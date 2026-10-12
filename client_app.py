from pathlib import Path
import sys
import pandas as pd
import streamlit as st
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

# Apply the main project theme
apply_2026_theme(page_title="Employment & Salary Prediction Portal", page_icon="🎓")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_dark_background(png_file):
    try:
        bin_str = get_base64_of_bin_file(png_file)
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
    except Exception:
        pass

# Apply the professional background image with dark overlay
bg_path = ROOT / "res" / "background.jpg"
if bg_path.exists():
    set_dark_background(bg_path)

st.markdown("<h1 style='text-align: center;'>🎓 Graduate Employment & Salary Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em; color: #cbd5e1;'>Welcome to our advanced predictive engine. Evaluate candidate profiles to forecast employment outcomes and starting salary.</p>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def load_data():
    return pd.read_csv(PROCESSED_DATA)

df = load_data()

@st.cache_resource
def get_statistical_salary_estimator():
    try:
        from sklearn.linear_model import LinearRegression
        data_df = pd.read_csv(PROCESSED_DATA)
        emp_df = data_df[data_df['employment_status'] == 'Employed'].dropna(subset=['salary'])
        features = ['gpa', 'age', 'education_level', 'field_of_study', 'internship_experience']
        X = pd.get_dummies(emp_df[features], drop_first=True)
        y = emp_df['salary']
        reg = LinearRegression().fit(X, y)
        cols = X.columns.tolist()
        return reg, cols
    except Exception:
        return None, []

def estimate_salary_for_candidate(candidate_df):
    reg, cols = get_statistical_salary_estimator()
    if reg is not None and cols:
        try:
            cand_features = candidate_df[['gpa', 'age', 'education_level', 'field_of_study', 'internship_experience']]
            X_cand = pd.get_dummies(cand_features)
            X_aligned = pd.DataFrame(0.0, index=[0], columns=cols)
            for c in cols:
                if c in X_cand.columns:
                    X_aligned[c] = float(X_cand[c].values[0])
                elif c in cand_features.columns:
                    X_aligned[c] = float(cand_features[c].values[0])
            pred = float(reg.predict(X_aligned)[0])
            if pred > 0:
                return pred
        except Exception:
            pass
    # Degree median baseline fallback
    try:
        data_df = pd.read_csv(PROCESSED_DATA)
        edu = candidate_df['education_level'].iloc[0]
        emp_df = data_df[data_df['employment_status'] == 'Employed']
        val = emp_df[emp_df['education_level'] == edu]['salary'].median()
        if not pd.isna(val) and val > 0:
            return float(val)
    except Exception:
        pass
    return 65000.0

with st.container():
    st.subheader("📝 Candidate Profile Input")
    inputs = employment_form(df)
    
st.divider()

if st.button("🚀 Calculate Employment Probability", type="primary", use_container_width=True):
    with st.spinner("Analyzing candidate profile against historical data..."):
        # Cross-platform Rscript path with automatic fallback
        if platform.system() == "Windows":
            default_path = r"E:\R-4.6.1\bin\Rscript.exe"
            import shutil
            RSCRIPT_PATH = default_path if Path(default_path).exists() else (shutil.which("Rscript") or "Rscript")
        else:
            RSCRIPT_PATH = "Rscript"
        
        script_path = str(ROOT / "R" / "predict_new.R")
        inputs_json = inputs.to_json(orient='records')
        
        try:
            result = subprocess.run(
                [RSCRIPT_PATH, script_path, inputs_json], 
                capture_output=True, text=True, check=True,
                cwd=str(ROOT)
            )
            
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
            predicted_salary = None
            if isinstance(raw_salary, (int, float)):
                predicted_salary = float(raw_salary) if float(raw_salary) > 0 else None
            elif isinstance(raw_salary, dict) and raw_salary:
                vals = [float(v) for v in raw_salary.values() if isinstance(v, (int, float)) and float(v) > 0]
                predicted_salary = vals[0] if vals else None
            elif isinstance(raw_salary, list) and raw_salary:
                vals = [float(v) for v in raw_salary if isinstance(v, (int, float)) and float(v) > 0]
                predicted_salary = vals[0] if vals else None
        except FileNotFoundError:
            st.error("⚠️ **Could not find Rscript!** Please ensure R is installed and configured in your environment PATH.")
            st.stop()
        except subprocess.CalledProcessError as e:
            st.error(f"Error connecting to R backend: {e}")
            if e.stderr:
                st.error(f"R Output: {e.stderr}")
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
                st.success("### 🎉 Positive Classification (Employed)")
                # Ensure salary is always computed and displayed for Employed classification
                if predicted_salary is None or predicted_salary <= 0:
                    predicted_salary = estimate_salary_for_candidate(inputs)
                st.metric("Estimated Starting Salary (Linear Regression)", f"${predicted_salary:,.2f}")
                st.markdown(
                    "**Statistical Inference:** The candidate is classified as **Employed** "
                    "with a predicted probability exceeding the 50% decision threshold.\n\n"
                    "**Model Architecture:**\n"
                    "- **Employment Status:** Evaluated using **Random Forest** (decision tree ensemble), modeling interactions between degree level, university ranking, GPA, and internships.\n"
                    "- **Starting Salary:** Projected using **Multiple Linear Regression**, benchmarked on historical graduate compensation data."
                )
            else:
                st.error("### ⚠️ Negative Classification (Unemployed/Other)")
                st.metric("Estimated Starting Salary", "N/A (Unemployed)")
                st.markdown(
                    "**Statistical Inference:** The candidate is classified as **Unemployed/Other** "
                    "as the predicted employment probability falls below the 50% decision threshold.\n\n"
                    "**Model Architecture:**\n"
                    "- **Employment Status:** Evaluated using **Random Forest** (decision tree ensemble) based on academic profile and employment trends.\n"
                    "- **Starting Salary:** Not Applicable. The regression model models active employment compensation, which does not apply to unemployed candidates."
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
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=280, margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.info("⚠️ **Disclaimer:** This is a model-based estimate generated from historical associations. It should not be used as an absolute individual employability label.")
