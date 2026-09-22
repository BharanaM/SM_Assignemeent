from pathlib import Path
import sys
import joblib
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.config import PROCESSED_DATA, MODEL_DIR, TABLE_DIR

# Set a wide, premium layout
st.set_page_config(page_title="Graduate Employment Analytics", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# Inject Custom CSS to make it look like a high-end application
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #1E3A8A; font-weight: 700; }
    div[data-testid="stMetricValue"] { font-size: 2rem; color: #1E3A8A; }
    .stMetric { background-color: #F8FAFC; padding: 15px; border-radius: 10px; border: 1px solid #E2E8F0; box-shadow: 2px 2px 5px rgba(0,0,0,0.02); }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv(PROCESSED_DATA)

def filtered_data(df):
    with st.sidebar:
        st.header("🎯 Dashboard Filters")
        st.markdown("Refine the dashboard based on student demographics.")
        
        # Use expanders to make the sidebar look clean and organized
        with st.expander("🎓 Academic Background", expanded=True):
            ed_opts = sorted(df["education_level"].dropna().unique())
            ed_sel = st.multiselect("Education Level", ed_opts, default=ed_opts)
            
            field_opts = sorted(df["field_of_study"].dropna().unique())
            field_sel = st.multiselect("Field of Study", field_opts, default=field_opts)
            
        with st.expander("🌍 Demographics", expanded=False):
            region_opts = sorted(df["region_of_study"].dropna().unique())
            region_sel = st.multiselect("Region of Study", region_opts, default=region_opts)
            
            gender_opts = sorted(df["gender"].dropna().unique())
            gender_sel = st.multiselect("Gender", gender_opts, default=gender_opts)
            
        # Apply filters
        df = df[df["education_level"].isin(ed_sel) & 
                df["field_of_study"].isin(field_sel) & 
                df["region_of_study"].isin(region_sel) &
                df["gender"].isin(gender_sel)]
    return df

def main():
    st.title("🎓 Graduate Employment Executive Dashboard")
    st.markdown("Welcome to the predictive analytics platform for graduate employment outcomes. Explore historical associations, academic performance metrics, and predictive insights below.")
    st.divider()
    
    if not PROCESSED_DATA.exists():
        st.error("⚠️ Data not found. Run `python scripts\\10_run_all.py` before opening the dashboard.")
        return
        
    df = filtered_data(load_data())
    
    # --- Top-Level Premium Metrics ---
    cols = st.columns(4)
    emp_rate = (df.employment_status == 'Employed').mean()
    intern_rate = (df.internship_experience == 'Yes').mean()
    
    cols[0].metric("Total Graduates", f"{len(df):,}")
    cols[1].metric("Employment Rate", f"{emp_rate:.1%}")
    cols[2].metric("Median GPA", f"{df.gpa.median():.2f}")
    cols[3].metric("Internship Experience Rate", f"{intern_rate:.1%}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- Main High-Quality Visualizations ---
    left, right = st.columns(2)
    
    with left:
        st.markdown("### 📊 Employment Status Breakdown")
        # Replace basic bar chart with a beautiful Plotly Donut Chart
        emp_counts = df.employment_status.value_counts().reset_index()
        emp_counts.columns = ['Status', 'Count']
        fig_emp = px.pie(emp_counts, values='Count', names='Status', hole=0.4, 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_emp.update_traces(textinfo='percent+label')
        fig_emp.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_emp, use_container_width=True)
        
        st.markdown("### 📚 Employment by Education Level")
        # Replace boring dataframe with a professional Stacked Bar Chart
        ed_cross = pd.crosstab(df.education_level, df.employment_status, normalize="index").mul(100).round(1).reset_index()
        ed_melt = ed_cross.melt(id_vars="education_level", var_name="Status", value_name="Percentage")
        fig_ed = px.bar(ed_melt, x="education_level", y="Percentage", color="Status", text="Percentage",
                        color_discrete_sequence=px.colors.qualitative.Set2)
        fig_ed.update_traces(texttemplate='%{text}%', textposition='inside')
        fig_ed.update_layout(xaxis_title="", yaxis_title="Percentage (%)", barmode='stack', margin=dict(t=20))
        st.plotly_chart(fig_ed, use_container_width=True)

    with right:
        st.markdown("### 📈 Impact of GPA on Employment")
        # Replace the old salary line chart with a highly analytical GPA Box Plot
        fig_gpa = px.box(df, x="employment_status", y="gpa", color="employment_status",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_gpa.update_layout(xaxis_title="", yaxis_title="Cumulative GPA", showlegend=False, margin=dict(t=20))
        st.plotly_chart(fig_gpa, use_container_width=True)
        
        st.markdown("### 🔬 Key Statistical Insights")
        # Put findings in a premium bordered container
        results_path = Path(__file__).resolve().parents[2] / "res" / "all_results.csv"
        if results_path.exists():
            results = pd.read_csv(results_path)
            with st.container(border=True):
                for _, row in results.head(5).iterrows():
                    p = row.get("Formatted_Adj_P_Value", "")
                    st.markdown(f"**{row['Research_Question']}**<br>↳ *Significance:* `p = {p}` | *Effect Magnitude:* `{row['Effect_Magnitude']}`", unsafe_allow_html=True)

    st.info("💡 **Note:** The current dataset does not contain a comprehensive soft-skills measurement battery. Factors like communication, teamwork, and leadership are not accounted for in these visualisations.")

if __name__ == "__main__":
    main()
