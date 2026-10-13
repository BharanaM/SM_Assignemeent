from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.config import PROCESSED_DATA

from app.components.ui_config import (
    apply_2026_theme,
    render_hero_banner,
    render_kpi_card,
    style_plotly_chart,
)

apply_2026_theme(page_title="Project Overview", page_icon="📄")

render_hero_banner(
    title="Project Overview & Industry Problem Statement",
    subtitle="Addressing graduate employment uncertainty across N = 299,984 global graduates through descriptive analytics, hypothesis testing, penalized & ensemble predictive modeling, and decision-support tools.",
    badges=[
        ("📄 Tasks 1–3: Domain & Dataset", ""),
        ("🏛️ Higher Education Consultancy", "cyan"),
        ("📊 15 Variables (11 Cat, 4 Num)", "emerald"),
    ],
)

df = pd.read_csv(PROCESSED_DATA)

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Clean Graduate Records", f"{len(df):,}", "16 exact duplicates removed", "👥", "#8b5cf6", "purple")
with c2:
    render_kpi_card("Observed Employment Rate", f"{(df.employment_status == 'Employed').mean():.1%}", "204,101 Employed Graduates", "💼", "#10b981")
with c3:
    render_kpi_card("Global Study Regions", f"{df.region_of_study.nunique()} Regions", "US, UK, Canada, EU, Asia, AU", "🌍", "#3b82f6", "blue")
with c4:
    render_kpi_card("Academic Disciplines", f"{df.field_of_study.nunique()} Fields", "Engineering, IT, Health, Business+", "🎓", "#f59e0b", "amber")

st.markdown("<br>", unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    with st.container(border=True):
        st.markdown(
            """
            <div class="section-header">
                <span class="section-title">💼 Employment Rate by Academic Discipline</span>
                <span class="section-tag">Cramer's V = 0.119</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        field_cross = (
            pd.crosstab(df.field_of_study, df.employment_status, normalize="index")
            .mul(100)
            .round(1)
            .reset_index()
        )
        field_melt = field_cross.melt(id_vars="field_of_study", var_name="Status", value_name="Percentage")
        field_melt["Status_Clean"] = field_melt["Status"].replace({"Not_Employed": "Not Employed"})
        fig_field = px.bar(
            field_melt,
            x="field_of_study",
            y="Percentage",
            color="Status_Clean",
            text="Percentage",
            barmode="group",
            color_discrete_map={"Employed": "#8b5cf6", "Not Employed": "#3b82f6"},
        )
        fig_field.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_field.update_layout(xaxis_title="", yaxis_title="Percentage (%)")
        fig_field = style_plotly_chart(fig_field, height=340)
        st.plotly_chart(fig_field, use_container_width=True)

with right:
    with st.container(border=True):
        st.markdown(
            """
            <div class="section-header">
                <span class="section-title">🎓 Employment Rate by University Ranking Tier</span>
                <span class="section-tag">Cramer's V = 0.374</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        rank_cross = (
            pd.crosstab(df.university_ranking, df.employment_status, normalize="index")
            .mul(100)
            .round(1)
            .reset_index()
        )
        rank_melt = rank_cross.melt(id_vars="university_ranking", var_name="Status", value_name="Percentage")
        rank_melt["Status_Clean"] = rank_melt["Status"].replace({"Not_Employed": "Not Employed"})
        fig_rank = px.bar(
            rank_melt,
            x="university_ranking",
            y="Percentage",
            color="Status_Clean",
            text="Percentage",
            barmode="stack",
            color_discrete_map={"Employed": "#10b981", "Not Employed": "#f43f5e"},
        )
        fig_rank.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
        fig_rank.update_layout(xaxis_title="University Reputation Tier", yaxis_title="Percentage (%)")
        fig_rank = style_plotly_chart(fig_rank, height=340)
        st.plotly_chart(fig_rank, use_container_width=True)
