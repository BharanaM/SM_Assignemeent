
import pandas as pd
import streamlit as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# joblib removed because we are using R for the backend now!


def employment_form(df):
    values = {}
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 👤 Demographics")
        values["age"] = st.number_input("Age", value=int(df["age"].median()), step=1)
        values["gender"] = st.selectbox("Gender", sorted(df["gender"].dropna().unique()))
        values["country_of_origin"] = st.selectbox("Country Of Origin", sorted(df["country_of_origin"].dropna().unique()))
        values["visa_type"] = st.selectbox("Visa Type", sorted(df["visa_type"].dropna().unique()))
        
    with col2:
        st.markdown("#### 🎓 Education")
        values["education_level"] = st.selectbox("Education Level", sorted(df["education_level"].dropna().unique()))
        values["field_of_study"] = st.selectbox("Field Of Study", sorted(df["field_of_study"].dropna().unique()))
        values["university_ranking"] = st.selectbox("University Ranking", sorted(df["university_ranking"].dropna().unique()))
        values["gpa"] = st.number_input("Gpa", value=float(df["gpa"].median()), step=0.01, format="%.2f")
        
    with col3:
        st.markdown("#### 💼 Experience & Skills")
        values["internship_experience"] = st.selectbox("Internship Experience", sorted(df["internship_experience"].dropna().unique()))
        values["language_proficiency"] = st.selectbox("Language Proficiency", sorted(df["language_proficiency"].dropna().unique()))
        values["region_of_study"] = st.selectbox("Region Of Study", sorted(df["region_of_study"].dropna().unique()))
        values["years_since_graduation"] = st.number_input("Years Since Graduation", value=int(df["years_since_graduation"].median()), step=1)
        
    return pd.DataFrame([values])
