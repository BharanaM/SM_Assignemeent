from pathlib import Path
import sys
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.config import FIGURE_DIR

from app.components.ui_config import (
    apply_2026_theme,
    render_hero_banner,
    render_kpi_card,
)

apply_2026_theme(page_title="Exploratory Analysis", page_icon="📊")

render_hero_banner(
    title="Exploratory Data Analysis & Data Quality Audit",
    subtitle="Comprehensive distributional profiling, structural missingness verification, and outlier diagnostics generated from our R statistical pipeline (R/01_cleaning_and_eda.R).",
    badges=[
        ("📊 Task 3: Descriptive Analytics", ""),
        ("🧹 16 Duplicates Removed", "cyan"),
        ("🔍 Structural Missingness Isolated", "emerald"),
    ],
)

k1, k2, k3, k4 = st.columns(4)
with k1:
    render_kpi_card("Raw → Clean Records", "299,984", "From 300,000 initial rows", "🧹", "#8b5cf6", "purple")
with k2:
    render_kpi_card("Structural Missingness", "100% Explained", "Salary & Job Sector for Unemployed", "🧩", "#10b981")
with k3:
    render_kpi_card("Age & GPA Outliers", "Retained", "Natural population variance (IQR)", "📏", "#3b82f6", "blue")
with k4:
    render_kpi_card("R Publication Plots", "12 Figures", "Exported to outputs/figures/", "🖼️", "#f59e0b", "amber")

st.markdown("<br>", unsafe_allow_html=True)

figures_dir = FIGURE_DIR

if figures_dir.exists() and any(figures_dir.iterdir()):
    image_files = sorted([f for f in figures_dir.glob("*.png")])

    if image_files:
        image_names = {f.stem.replace("_", " ").title(): f for f in image_files}

        tab1, tab2, tab3 = st.tabs(["🖼️ R Publication Gallery", "🔍 High-Res Focus Inspector", "📝 Data Quality & Missingness Tables"])

        with tab1:
            cols = st.columns(2)
            for i, (name, path) in enumerate(image_names.items()):
                with cols[i % 2]:
                    with st.container(border=True):
                        st.image(str(path), use_container_width=True)
                        st.markdown(f"<div class='gallery-caption'>{name}</div>", unsafe_allow_html=True)

        with tab2:
            col1, col2 = st.columns([1, 2.6])
            with col1:
                with st.container(border=True):
                    selected_name = st.radio("Select R Visualization:", list(image_names.keys()))
            with col2:
                selected_file = image_names[selected_name]
                with st.container(border=True):
                    st.image(str(selected_file), use_container_width=True)
                    st.markdown(f"<div class='gallery-caption'>{selected_name}</div>", unsafe_allow_html=True)

        with tab3:
            col_a, col_b = st.columns(2)
            with col_a:
                with st.container(border=True):
                    st.markdown("#### Missing Value Audit")
                    try:
                        missing_df = pd.read_csv(figures_dir.parent / "tables" / "missing_value_summary.csv")
                        st.dataframe(missing_df, use_container_width=True, hide_index=True)
                        st.caption("📌 `salary` and `job_sector` are structurally NA for non-employed graduates.")
                    except Exception:
                        st.warning("Could not load missing_value_summary.csv")

            with col_b:
                with st.container(border=True):
                    st.markdown("#### Numeric Summary & IQR Bounds")
                    try:
                        num_df = pd.read_csv(figures_dir.parent / "tables" / "numerical_summary.csv")
                        st.dataframe(num_df, use_container_width=True, hide_index=True)
                    except Exception:
                        st.warning("Could not load numerical_summary.csv")
    else:
        st.warning("No PNG visualizations found in outputs/figures directory.")
else:
    st.error(f"Could not find the figures directory at: {figures_dir}")
