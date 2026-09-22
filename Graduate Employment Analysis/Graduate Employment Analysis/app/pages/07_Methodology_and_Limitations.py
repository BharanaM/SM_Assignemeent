import streamlit as st

st.set_page_config(page_title="Methodology & Limitations", page_icon="📘", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #1E3A8A; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

st.title("📘 Methodology & Limitations")
st.markdown("Understanding the design boundaries and analytical approach of this platform.")

with st.expander("🛠️ Data Processing Methodology", expanded=True):
    st.markdown("""
    * **Deduplication:** The pipeline aggressively identifies and removes exact duplicate rows to maintain statistical integrity.
    * **Data Retention:** Observed categories are retained as-is, while suspicious outlier values are automatically reported in the data quality reports.
    * **Predictor Selection:** Variables that occur *post-employment* (such as Job Sector and Salary) are strictly excluded from the Employment Prediction models to prevent data leakage.
    """)

with st.expander("⚠️ Analytical Limitations", expanded=True):
    st.markdown("""
    * **Soft Skills Deficit:** The current dataset lacks a comprehensive measurement battery for soft skills. Vital employability factors such as communication, teamwork, and leadership cannot be directly estimated from these metrics alone.
    * **Observational Restraints:** The provided data is purely observational. All models and statistical tests represent *associations* and **should not be interpreted as causal effects**.
    """)

with st.expander("🔮 Future Extensions", expanded=False):
    st.markdown("""
    Advanced modeling techniques such as Principal Component Analysis (PCA), Bayesian modeling, experimental designs, and time-series tracking currently require longitudinal datasets that extend beyond the scope of this cross-sectional file.
    """)
