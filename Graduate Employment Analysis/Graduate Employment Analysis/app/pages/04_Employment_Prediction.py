from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.config import PROCESSED_DATA, MODEL_DIR
from app.components.model_ui import employment_form, model

st.set_page_config(page_title="Employment Prediction", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #1E3A8A; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

st.title("🔮 Predictive Employment Engine")
st.markdown("Use the form below to input a graduate's profile. The machine learning model will calculate the exact probability of this candidate securing employment based on historical trends.")

df = pd.read_csv(PROCESSED_DATA)

with st.container(border=True):
    st.subheader("📝 Candidate Profile Input")
    inputs = employment_form(df)
    
st.divider()

if st.button("🚀 Calculate Employment Probability", type="primary", use_container_width=True):
    with st.spinner("Analyzing candidate profile..."):
        fitted = model("employment_model.joblib")
        probability = fitted.predict_proba(inputs)[0]
        emp_prob = probability[1]
        
        st.markdown("### 🎯 Prediction Results")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if emp_prob >= 0.5:
                st.success(f"### 🎉 Employed")
                st.markdown("This candidate has a strong profile and is likely to be employed.")
            else:
                st.error(f"### ⚠️ Not Employed")
                st.markdown("This candidate is at high risk of remaining unemployed or continuing education.")
                
        with col2:
            st.markdown(f"**Likelihood of Employment:** `{emp_prob:.1%}`")
            st.progress(float(emp_prob))
            st.markdown(f"**Likelihood of Non-Employment:** `{probability[0]:.1%}`")
            st.progress(float(probability[0]))

st.markdown("<br><br>", unsafe_allow_html=True)
st.warning("⚠️ **Disclaimer:** This is a model-based estimate generated from historical associations. It should not be used as an absolute individual employability label.")
