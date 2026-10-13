import pandas as pd
import streamlit as st


def employment_form(df):
    st.markdown("#### ⚡ Quick Presets (1-Click Demo Profiles)")
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)

    preset = None
    with p_col1:
        if st.button("🌟 High-Potential Master's", use_container_width=True):
            preset = {
                "age": 26,
                "gender": "Female",
                "country_of_origin": "India",
                "visa_type": "Post-study",
                "education_level": "Master's",
                "field_of_study": "IT",
                "university_ranking": "High",
                "gpa": 3.85,
                "internship_experience": "Yes",
                "language_proficiency": "Fluent",
                "region_of_study": "US",
                "years_since_graduation": 1,
            }
    with p_col2:
        if st.button("⚠️ At-Risk Candidate", use_container_width=True):
            preset = {
                "age": 23,
                "gender": "Male",
                "country_of_origin": "Brazil",
                "visa_type": "Student",
                "education_level": "Bachelor's",
                "field_of_study": "Arts",
                "university_ranking": "Low",
                "gpa": 2.65,
                "internship_experience": "No",
                "language_proficiency": "Basic",
                "region_of_study": "Asia",
                "years_since_graduation": 1,
            }
    with p_col3:
        if st.button("🔬 PhD Research Scholar", use_container_width=True):
            preset = {
                "age": 29,
                "gender": "Male",
                "country_of_origin": "Germany",
                "visa_type": "Permanent Residency",
                "education_level": "PhD",
                "field_of_study": "Engineering",
                "university_ranking": "High",
                "gpa": 3.92,
                "internship_experience": "Yes",
                "language_proficiency": "Fluent",
                "region_of_study": "EU",
                "years_since_graduation": 2,
            }
    with p_col4:
        if st.button("🔄 Reset Defaults", use_container_width=True):
            preset = {}

    if preset:
        st.session_state["cand_profile"] = preset

    curr = st.session_state.get("cand_profile", {})

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    def get_val(key, default):
        return curr.get(key, default)

    def get_idx(key, opts, default_val):
        val = curr.get(key, default_val)
        return opts.index(val) if val in opts else 0

    values = {}

    with col1:
        st.markdown("##### 👤 Demographics & Background")
        values["age"] = st.number_input("Age (Years)", min_value=20, max_value=50, value=int(get_val("age", int(df["age"].median()))), step=1)
        gender_opts = sorted(df["gender"].dropna().unique())
        values["gender"] = st.selectbox("Gender", gender_opts, index=get_idx("gender", gender_opts, "Female"))
        country_opts = sorted(df["country_of_origin"].dropna().unique())
        values["country_of_origin"] = st.selectbox("Country of Origin", country_opts, index=get_idx("country_of_origin", country_opts, country_opts[0]))
        visa_opts = sorted(df["visa_type"].dropna().unique())
        values["visa_type"] = st.selectbox("Visa Classification", visa_opts, index=get_idx("visa_type", visa_opts, visa_opts[0]))

    with col2:
        st.markdown("##### 🎓 Academic Qualifications")
        edu_opts = sorted(df["education_level"].dropna().unique())
        values["education_level"] = st.selectbox("Degree Level", edu_opts, index=get_idx("education_level", edu_opts, "Bachelor's"))
        field_opts = sorted(df["field_of_study"].dropna().unique())
        values["field_of_study"] = st.selectbox("Academic Discipline", field_opts, index=get_idx("field_of_study", field_opts, "IT"))
        rank_opts = sorted(df["university_ranking"].dropna().unique())
        values["university_ranking"] = st.selectbox("Institutional Tier", rank_opts, index=get_idx("university_ranking", rank_opts, "Medium"))
        values["gpa"] = st.number_input("Cumulative GPA", min_value=1.0, max_value=4.0, value=float(get_val("gpa", float(df["gpa"].median()))), step=0.05, format="%.2f")

    with col3:
        st.markdown("##### 💼 Practical Skills & Experience")
        intern_opts = sorted(df["internship_experience"].dropna().unique())
        values["internship_experience"] = st.selectbox("Completed Internship?", intern_opts, index=get_idx("internship_experience", intern_opts, "Yes"))
        lang_opts = sorted(df["language_proficiency"].dropna().unique())
        values["language_proficiency"] = st.selectbox("Language Fluency", lang_opts, index=get_idx("language_proficiency", lang_opts, "Fluent"))
        region_opts = sorted(df["region_of_study"].dropna().unique())
        values["region_of_study"] = st.selectbox("Region of Study", region_opts, index=get_idx("region_of_study", region_opts, region_opts[0]))
        values["years_since_graduation"] = st.number_input("Years Since Degree", min_value=0, max_value=15, value=int(get_val("years_since_graduation", int(df["years_since_graduation"].median()))), step=1)

    return pd.DataFrame([values])
