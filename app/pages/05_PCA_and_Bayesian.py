import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.config import FIGURE_DIR

from app.components.ui_config import apply_2026_theme
apply_2026_theme(page_title="PCA & Bayesian Inference", page_icon="📈")

st.markdown('''
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #1E3A8A; font-weight: 700; }
    h2, h3 { color: #2563EB; }
    </style>
''', unsafe_allow_html=True)

st.title("📈 PCA & Bayesian Inference (Tasks 7 & 8)")
st.markdown("This section details the advanced mathematical approaches utilized for dimensionality reduction and probabilistic classification, aligning with our final consultancy report.")

tab1, tab2 = st.tabs(["📉 Principal Component Analysis (Task 7)", "🧮 Bayesian Methods (Task 8)"])

with tab1:
    st.header("Dimensionality Reduction via PCA")
    st.markdown("Principal Component Analysis (PCA) was performed on the continuous numeric predictors (`age`, `years_since_graduation`, `gpa`).")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.subheader("Evidence Against PCA")
        st.markdown('''
        * **Correlation Matrix:** The highest correlation among predictors is negligible (r < 0.1), meaning there is no multicollinearity to compress.
        * **Kaiser Criterion:** Running PCA yielded three components, but variance is spread evenly (approx. 35.8%, 33.3%, 30.8%). There is no single dominant component.
        * **Prediction Impact:** A PCA-based logistic regression performed no better than the original variables, while completely obfuscating the meaning of the coefficients.
        * **Categorical Data Constraint:** PCA relies on continuous variance and Euclidean distance. Because 11 of our 15 variables are categorical, **Factor Analysis of Mixed Data (FAMD)** or Multiple Correspondence Analysis (MCA) would be the mathematically correct alternatives.
        ''')
            
    with col_b:
        st.info("**Final Conclusion:** We explicitly rejected PCA for our final models because **interpretability matters for management**. Predicting employment based on mathematical abstractions like 'PC1' is useless for career advisors, who need to know the direct, actionable impact of tangible metrics like GPA and internships.")

with tab2:
    st.header("Bayesian Methods (Task 8)")
    st.markdown("Bayesian methods update prior beliefs with observed data to form a posterior probability distribution, outputting exact probability statements about risk and success.")
    
    col_x, col_y = st.columns([1, 1])
    
    with col_x:
        st.subheader("1. Naïve Bayes & Bayesian Regression")
        st.markdown('''
        * **Naïve Bayes:** Evaluated and added to our model comparison metrics. While computationally fast, its strict assumption of feature independence is a limitation given natural correlations in demographics.
        * **Bayesian Logistic Regression (rstanarm):** We ran an MCMC simulation to generate posterior distributions. The 95% credible intervals for the internship coefficient confirmed a strong positive effect, providing a probabilistic distribution of the effect size rather than a single point estimate.
        ''')
        
    with col_y:
        st.subheader("2. Bayesian Decision Making (Beta-Binomial)")
        st.markdown('''
        To model the value of an internship, we used a uniform **Beta(1,1)** prior. Updating this with our data yielded two posterior Beta distributions. 
        
        A simulation of 100,000 draws from these posteriors revealed a **100% probability (Prob = 1.0)** that the employment rate for graduates with internships is higher than for those without. 
        ''')
        
    st.success("**Honest Limits:** The primary challenges of Bayesian methods in this context are computational cost (MCMC sampling on 300,000 rows takes hours compared to seconds for frequentist MLE), the subjective choice of priors, and the difficulty of communicating posterior credible intervals to non-statistician administrators.")
