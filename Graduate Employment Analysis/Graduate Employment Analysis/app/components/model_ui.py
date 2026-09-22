import joblib
import pandas as pd
import streamlit as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

@st.cache_resource
def model(name):
    return joblib.load(ROOT / "models" / name)

def employment_form(df):
    values = {}
    for col in ["country_of_origin", "education_level", "field_of_study", "language_proficiency",
                "visa_type", "gender", "university_ranking", "region_of_study", "internship_experience"]:
        values[col] = st.selectbox(col.replace("_", " ").title(), sorted(df[col].dropna().unique()))
    for col in ["age", "years_since_graduation", "gpa"]:
        values[col] = st.number_input(col.replace("_", " ").title(), value=float(df[col].median()))
    return pd.DataFrame([values])
