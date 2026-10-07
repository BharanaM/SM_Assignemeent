from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.config import PROCESSED_DATA

from app.components.ui_config import apply_2026_theme
apply_2026_theme(page_title="Project Overview", page_icon="📄")

st.title("📄 Project Overview")
st.markdown("This dashboard provides a comprehensive analysis of graduate employment trends based on a dataset of nearly 300,000 graduates. Below is a high-level summary of the dataset's current state.")

df = pd.read_csv(PROCESSED_DATA)

# Top Metrics
st.markdown("### 📌 Key Dataset Metrics")
cols = st.columns(3)
cols[0].metric("Total Graduates Tracked", f"{len(df):,}")
cols[1].metric("Observed Employment Rate", f"{(df.employment_status == 'Employed').mean():.1%}")
cols[2].metric("Global Regions Represented", f"{df.region_of_study.nunique()}")

st.divider()

left, right = st.columns(2)

with left:
    st.markdown("### 💼 Overall Employment Distribution")
    emp_counts = df.employment_status.value_counts().reset_index()
    emp_counts.columns = ['Status', 'Count']
    fig_emp = px.bar(emp_counts, x='Status', y='Count', color='Status', text='Count',
                     color_discrete_sequence=["#8b5cf6", "#3b82f6", "#ec4899", "#14b8a6", "#f59e0b", "#f43f5e"])
    fig_emp.update_traces(textposition='outside')
    fig_emp.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False, xaxis_title="", yaxis_title="Number of Graduates")
    st.plotly_chart(fig_emp, use_container_width=True)

with right:
    st.markdown("### 🎓 Employment by Degree Type")
    ed_cross = pd.crosstab(df.education_level, df.employment_status, normalize="index").mul(100).round(1).reset_index()
    ed_melt = ed_cross.melt(id_vars="education_level", var_name="Status", value_name="Percentage")
    fig_ed = px.bar(ed_melt, x="education_level", y="Percentage", color="Status", text="Percentage",
                    color_discrete_sequence=["#8b5cf6", "#3b82f6", "#ec4899", "#14b8a6", "#f59e0b", "#f43f5e"])
    fig_ed.update_traces(texttemplate='%{text}%', textposition='inside')
    fig_ed.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis_title="Education Level", yaxis_title="Employment %", barmode='stack')
    st.plotly_chart(fig_ed, use_container_width=True)

st.info("💡 **Tip:** Use the 'Exploratory Analysis' page to dig deeper into how these metrics correlate with specific numerical and categorical factors!")
