from pathlib import Path
import sys
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.config import FIGURE_DIR

from app.components.ui_config import apply_2026_theme
apply_2026_theme(page_title="Exploratory Analysis", page_icon="📊")



st.title("📊 Exploratory Data Analysis")
st.markdown("Explore the distributions and relationships in the graduate dataset. These visualizations were generated directly from our R statistical analysis scripts.")

figures_dir = FIGURE_DIR

if figures_dir.exists() and any(figures_dir.iterdir()):
    image_files = sorted([f for f in figures_dir.glob("*.png")])
    
    if image_files:
        image_names = {f.stem.replace("_", " ").title(): f for f in image_files}
        
        tab1, tab2, tab3 = st.tabs(["🖼️ Gallery View", "🔍 Focus View", "📝 Data Quality"])
        
        with tab1:
            st.markdown("### 🖼️ Overview Gallery")
            st.markdown("A bird's-eye view of all generated analysis plots.")
            
            # Create a 2-column grid
            cols = st.columns(2)
            for i, (name, path) in enumerate(image_names.items()):
                with cols[i % 2]:
                    with st.container(border=True):
                        st.image(str(path), use_container_width=True)
                        st.markdown(f"<div class='gallery-caption'>{name}</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### 🔍 Detailed Inspection")
            col1, col2 = st.columns([1, 3])
            with col1:
                selected_name = st.radio("Select Visualization:", list(image_names.keys()))
            with col2:
                selected_file = image_names[selected_name]
                with st.container(border=True):
                    st.image(str(selected_file), use_container_width=True)
                    st.markdown(f"<h4 style='text-align: center; color: #1E3A8A;'>{selected_name}</h4>", unsafe_allow_html=True)
        
        with tab3:
            st.markdown("### 📝 Data Quality & Diagnostics")
            import pandas as pd
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.subheader("Missing Value Summary")
                try:
                    missing_df = pd.read_csv(figures_dir.parent / "tables" / "missing_value_summary.csv")
                    st.dataframe(missing_df, use_container_width=True, hide_index=True)
                    st.info("Note: Salary and Job Sector are legitimately NA for Unemployed graduates.")
                except Exception as e:
                    st.warning("Could not load missing_value_summary.csv")
            
            with col_b:
                st.subheader("Outlier Detection (IQR)")
                try:
                    outlier_df = pd.read_csv(figures_dir.parent / "tables" / "outliers_summary.csv")
                    st.dataframe(outlier_df, use_container_width=True, hide_index=True)
                except Exception as e:
                    st.warning("Could not load outliers_summary.csv")
            
            st.divider()
            st.subheader("🔗 Numeric Correlation Matrix")
            try:
                corr_df = pd.read_csv(figures_dir.parent / "tables" / "correlation_matrix.csv")
                # Assume the first column is the variable names if it doesn't have an explicit name, but pandas read_csv handles it.
                st.dataframe(corr_df.style.background_gradient(cmap='coolwarm', axis=None), use_container_width=True)
            except Exception as e:
                st.warning("Could not load correlation_matrix.csv")
        
        st.divider()
        st.markdown("*Note: If you update the data, please run the `01_cleaning_and_eda.R` script again to regenerate these plots.*")
    else:
        st.warning("No PNG visualizations found in Outputs/figures directory.")
else:
    st.error(f"Could not find the figures directory at: {figures_dir}")
