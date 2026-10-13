from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px

pd.options.future.infer_string = False
pd.options.mode.string_storage = "python"

# Robust path handling for both local and Streamlit Community Cloud
APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent

for p in [str(ROOT), str(APP_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from src.config import PROCESSED_DATA
except Exception:
    PROCESSED_DATA = ROOT / "data" / "preprocessed" / "dataset_predictive.csv"

# Cloud-safe import: try direct components first to avoid Streamlit Cloud 'app' package namespace collisions
try:
    from components.ui_config import (
        apply_2026_theme,
        render_hero_banner,
        render_kpi_card,
        style_plotly_chart,
    )
except Exception:
    try:
        from app.components.ui_config import (
            apply_2026_theme,
            render_hero_banner,
            render_kpi_card,
            style_plotly_chart,
        )
    except Exception:
        # Fallback in case of cloud environment import isolation
        def apply_2026_theme(page_title="Analytics", page_icon="🎓"):
            st.set_page_config(page_title=page_title, page_icon=page_icon, layout="wide")

        def render_hero_banner(title: str, subtitle: str, badges=None):
            st.title(title)
            st.markdown(subtitle)

        def render_kpi_card(label: str, value: str, delta: str = "", icon: str = "📊", accent: str = "#8b5cf6", delta_cls: str = ""):
            st.metric(label, value, delta)

        def style_plotly_chart(fig, height=360, show_legend=True):
            fig.update_layout(height=height, showlegend=show_legend)
            return fig

# Apply 2026 futuristic dark theme
apply_2026_theme(page_title="Executive Graduate Analytics", page_icon="🎓")


@st.cache_data
def load_data():
    df = pd.read_csv(PROCESSED_DATA)
    for col in df.columns:
        if df[col].dtype == "string":
            df[col] = df[col].astype("object")
    return df


def filtered_data(df):
    with st.sidebar:
        st.markdown("### 🎯 Executive Filters")
        st.caption("Filter cohort data dynamically across all visualizations.")

        with st.expander("🎓 Academic Qualifications", expanded=True):
            ed_opts = sorted(df["education_level"].dropna().unique())
            ed_sel = st.multiselect("Education Level", ed_opts, default=ed_opts)

            field_opts = sorted(df["field_of_study"].dropna().unique())
            field_sel = st.multiselect("Field of Study", field_opts, default=field_opts)

        with st.expander("🌍 Geography & Demographics", expanded=False):
            region_opts = sorted(df["region_of_study"].dropna().unique())
            region_sel = st.multiselect("Region of Study", region_opts, default=region_opts)

            gender_opts = sorted(df["gender"].dropna().unique())
            gender_sel = st.multiselect("Gender", gender_opts, default=gender_opts)

            ranking_opts = sorted(df["university_ranking"].dropna().unique())
            ranking_sel = st.multiselect("University Ranking", ranking_opts, default=ranking_opts)

        with st.expander("💼 Experiential Attributes", expanded=False):
            intern_opts = sorted(df["internship_experience"].dropna().unique())
            intern_sel = st.multiselect("Internship Completed", intern_opts, default=intern_opts)

            lang_opts = sorted(df["language_proficiency"].dropna().unique())
            lang_sel = st.multiselect("Language Fluency", lang_opts, default=lang_opts)

        filtered = df[
            df["education_level"].isin(ed_sel)
            & df["field_of_study"].isin(field_sel)
            & df["region_of_study"].isin(region_sel)
            & df["gender"].isin(gender_sel)
            & df["university_ranking"].isin(ranking_sel)
            & df["internship_experience"].isin(intern_sel)
            & df["language_proficiency"].isin(lang_sel)
        ]

        st.divider()
        st.markdown(
            f"""
            <div style="background: rgba(139, 92, 246, 0.12); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 10px; padding: 0.75rem 0.9rem; font-size: 0.82rem; color: #ddd6fe;">
                <strong>⚡ Active Cohort Size:</strong><br>
                <span style="font-size: 1.15rem; font-weight: 700; color: #fff;">{len(filtered):,}</span> / {len(df):,} graduates ({len(filtered)/len(df):.1%})
            </div>
            """,
            unsafe_allow_html=True,
        )

    return filtered


def main():
    render_hero_banner(
        title="Graduate Employment Executive Command Center",
        subtitle="A full-spectrum predictive modeling and statistical intelligence suite. Moving university administration from reactive post-graduation surveys to proactive, data-driven early career intervention.",
        badges=[
            ("🎓 IT3081 Statistical Modeling", ""),
            ("⚡ Live R 4.6 Engine Active", "cyan"),
            ("📊 N = 299,984 Cohort", "emerald"),
            ("🎯 ROC-AUC: 0.957", "purple"),
        ],
    )

    if not Path(PROCESSED_DATA).exists():
        st.error("⚠️ Processed dataset not found. Please ensure data/preprocessed/dataset_predictive.csv exists.")
        return

    raw_df = load_data()
    df = filtered_data(raw_df)

    if df.empty:
        st.warning("⚠️ No graduates match the current filter selection. Please broaden your sidebar filters.")
        return

    # --- Top-Level Premium Metrics ---
    emp_df = df[df.employment_status == "Employed"]
    emp_rate = (df.employment_status == "Employed").mean()
    intern_rate = (df.internship_experience == "Yes").mean()
    med_salary = emp_df.salary.median() if not emp_df.empty else 0
    med_gpa = df.gpa.median()

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        render_kpi_card(
            label="Total Cohort",
            value=f"{len(df):,}",
            delta=f"{len(df)/len(raw_df):.0%} of total dataset",
            icon="👥",
            accent="#8b5cf6",
            delta_cls="purple",
        )
    with kpi2:
        render_kpi_card(
            label="Employment Rate",
            value=f"{emp_rate:.1%}",
            delta=f"{len(emp_df):,} Employed",
            icon="💼",
            accent="#10b981",
            delta_cls="",
        )
    with kpi3:
        render_kpi_card(
            label="Median Starting Salary",
            value=f"${med_salary:,.0f}" if med_salary > 0 else "N/A",
            delta="Employed baseline (excl. $0 NA)",
            icon="💵",
            accent="#3b82f6",
            delta_cls="blue",
        )
    with kpi4:
        render_kpi_card(
            label="Median GPA",
            value=f"{med_gpa:.2f}",
            delta=f"Mean: {df.gpa.mean():.2f} (2.0–4.0)",
            icon="📈",
            accent="#06b6d4",
            delta_cls="blue",
        )
    with kpi5:
        render_kpi_card(
            label="Internship Rate",
            value=f"{intern_rate:.1%}",
            delta="OR = 1.74 (+74.1% Odds)",
            icon="🎯",
            accent="#f59e0b",
            delta_cls="amber",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Primary Visualizations Grid ---
    main_tabs = st.tabs([
        "📊 Employment & Academic Drivers",
        "💰 Starting Salary Analytics (Employed)",
        "🔬 Key Statistical Inference Summary",
        "🏛️ Stakeholder Decision Matrix",
    ])

    with main_tabs[0]:
        left, right = st.columns(2)

        with left:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="section-header">
                        <span class="section-title">📊 Overall Employment Status Breakdown</span>
                        <span class="section-tag">Cohort Distribution</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                emp_counts = df.employment_status.value_counts().reset_index()
                emp_counts.columns = ["Status", "Count"]
                emp_counts["Status_Clean"] = emp_counts["Status"].replace({"Not_Employed": "Not Employed"})
                fig_emp = px.pie(
                    emp_counts,
                    values="Count",
                    names="Status_Clean",
                    hole=0.48,
                    color="Status_Clean",
                    color_discrete_map={
                        "Employed": "#8b5cf6",
                        "Not Employed": "#3b82f6",
                        "Continuing Education": "#06b6d4",
                        "Unemployed": "#f43f5e",
                    },
                )
                fig_emp.update_traces(
                    textinfo="percent+label",
                    textfont_size=13,
                    marker=dict(line=dict(color="#0f172a", width=2)),
                    hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
                )
                fig_emp = style_plotly_chart(fig_emp, height=330, show_legend=True)
                st.plotly_chart(fig_emp, use_container_width=True)
                st.caption("📌 **Insight:** Employment rate baseline is 68.0% Employed vs 32.0% Not Employed across the cleaned 299,984 cohort.")

            with st.container(border=True):
                st.markdown(
                    """
                    <div class="section-header">
                        <span class="section-title">📚 Employment Rate by Degree Level</span>
                        <span class="section-tag">Tier Progression</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                ed_cross = (
                    pd.crosstab(df.education_level, df.employment_status, normalize="index")
                    .mul(100)
                    .round(1)
                    .reset_index()
                )
                ed_melt = ed_cross.melt(id_vars="education_level", var_name="Status", value_name="Percentage")
                ed_melt["Status_Clean"] = ed_melt["Status"].replace({"Not_Employed": "Not Employed"})
                fig_ed = px.bar(
                    ed_melt,
                    x="education_level",
                    y="Percentage",
                    color="Status_Clean",
                    text="Percentage",
                    barmode="stack",
                    color_discrete_map={"Employed": "#8b5cf6", "Not Employed": "#3b82f6"},
                )
                fig_ed.update_traces(texttemplate="%{text:.1f}%", textposition="inside", textfont_size=12)
                fig_ed.update_layout(xaxis_title="", yaxis_title="Share (%)")
                fig_ed = style_plotly_chart(fig_ed, height=330)
                st.plotly_chart(fig_ed, use_container_width=True)
                st.caption("📌 **Insight:** Monotonic degree progression: PhD graduates achieve the highest employment rate (OR = 9.48 vs Bachelor's).")

        with right:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="section-header">
                        <span class="section-title">📈 GPA Distribution by Employment Status</span>
                        <span class="section-tag">Boxplot (IQR)</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                fig_gpa = px.box(
                    df,
                    x="employment_status",
                    y="gpa",
                    color="employment_status",
                    color_discrete_map={"Employed": "#8b5cf6", "Not_Employed": "#3b82f6"},
                )
                fig_gpa.update_layout(xaxis_title="", yaxis_title="Cumulative GPA (Scale: 4.0)")
                fig_gpa = style_plotly_chart(fig_gpa, height=330, show_legend=False)
                st.plotly_chart(fig_gpa, use_container_width=True)
                st.caption("📌 **Insight:** Employed graduates maintain significantly higher median GPA (3.54 vs 3.08, Welch's t-test p < 0.001, Cohen's d = 0.54).")

            with st.container(border=True):
                st.markdown(
                    """
                    <div class="section-header">
                        <span class="section-title">🎯 Employment Rate by Practical Internship</span>
                        <span class="section-tag">Cohen's h = 0.488</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                intern_cross = (
                    pd.crosstab(df.internship_experience, df.employment_status, normalize="index")
                    .mul(100)
                    .round(1)
                    .reset_index()
                )
                intern_melt = intern_cross.melt(id_vars="internship_experience", var_name="Status", value_name="Percentage")
                intern_melt["Status_Clean"] = intern_melt["Status"].replace({"Not_Employed": "Not Employed"})
                fig_intern = px.bar(
                    intern_melt,
                    x="internship_experience",
                    y="Percentage",
                    color="Status_Clean",
                    text="Percentage",
                    barmode="group",
                    color_discrete_map={"Employed": "#10b981", "Not Employed": "#f43f5e"},
                )
                fig_intern.update_traces(texttemplate="%{text:.1f}%", textposition="outside", textfont_size=12)
                fig_intern.update_layout(xaxis_title="Internship Completed?", yaxis_title="Share (%)")
                fig_intern = style_plotly_chart(fig_intern, height=330)
                st.plotly_chart(fig_intern, use_container_width=True)
                st.caption("📌 **Insight:** 71.6% of employed graduates had prior internship experience (Two-Proportion Z-Test p < 0.001).")

    with main_tabs[1]:
        sal_left, sal_right = st.columns(2)

        with sal_left:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="section-header">
                        <span class="section-title">💵 Starting Salary by Field of Study</span>
                        <span class="section-tag">ANOVA F-test p < 0.001</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if not emp_df.empty:
                    fig_sal_field = px.box(
                        emp_df,
                        x="field_of_study",
                        y="salary",
                        color="field_of_study",
                        color_discrete_sequence=["#8b5cf6", "#3b82f6", "#06b6d4", "#10b981", "#f59e0b", "#ec4899"],
                    )
                    fig_sal_field.update_layout(xaxis_title="", yaxis_title="Starting Salary (USD)")
                    fig_sal_field = style_plotly_chart(fig_sal_field, height=350, show_legend=False)
                    st.plotly_chart(fig_sal_field, use_container_width=True)
                    st.caption("📌 **Insight:** Technology ($98k+) and Finance lead starting salary distributions, followed by Engineering and Healthcare.")

        with sal_right:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="section-header">
                        <span class="section-title">🎓 Salary Premium by Education Level</span>
                        <span class="section-tag">Eta-squared η² = 0.458</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if not emp_df.empty:
                    fig_sal_edu = px.violin(
                        emp_df,
                        x="education_level",
                        y="salary",
                        color="education_level",
                        box=True,
                        points=False,
                        color_discrete_sequence=["#3b82f6", "#06b6d4", "#8b5cf6", "#10b981"],
                    )
                    fig_sal_edu.update_layout(xaxis_title="", yaxis_title="Starting Salary (USD)")
                    fig_sal_edu = style_plotly_chart(fig_sal_edu, height=350, show_legend=False)
                    st.plotly_chart(fig_sal_edu, use_container_width=True)
                    st.caption("📌 **Insight:** Large effect size (η² = 0.458) proves degree level explains 45.8% of salary variance among employed graduates.")

    with main_tabs[2]:
        with st.container(border=True):
            st.markdown(
                """
                <div class="section-header">
                    <span class="section-title">🔬 Rigorous Statistical Inference Output Table</span>
                    <span class="section-tag">Benjamini-Hochberg FDR Adjusted</span>
                </div>
                """,
                unsafe_allow_html=True,
                )
            inf_path = ROOT / "outputs" / "tables" / "inference_results.csv"
            if inf_path.exists():
                inf_df = pd.read_csv(inf_path)
                inf_df["P_Value_Fmt"] = inf_df["P_Value"].apply(lambda x: "< 0.001" if x == 0 or x < 0.001 else f"{x:.4f}")
                inf_df["Adj_P_Fmt"] = inf_df["Adjusted_P_Value"].apply(lambda x: "< 0.001" if x == 0 or x < 0.001 else f"{x:.4f}")

                show_cols = ["Test_Name", "Test_Used", "H0", "P_Value_Fmt", "Adj_P_Fmt", "Effect_Size_Metric", "Effect_Size_Value", "Practical_Meaning"]
                st.dataframe(
                    inf_df[show_cols].rename(columns={
                        "Test_Name": "Hypothesis Test",
                        "Test_Used": "Statistical Test",
                        "H0": "Null Hypothesis (H0)",
                        "P_Value_Fmt": "Raw p-value",
                        "Adj_P_Fmt": "BH-Adjusted p",
                        "Effect_Size_Metric": "Effect Metric",
                        "Effect_Size_Value": "Effect Size",
                        "Practical_Meaning": "Practical Significance",
                    }),
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("Inference table not found in outputs/tables/inference_results.csv. Run R/02_statistical_inference.R to generate.")

    with main_tabs[3]:
        st.markdown(
            """
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin-top: 0.5rem;">
                <div class="metric-card" style="border-left-color: #8b5cf6;">
                    <h4>🏛️ University Management</h4>
                    <p><strong>Primary Interest:</strong> Institutional global ranking, degree ROI, student retention.</p>
                    <p><strong>Decision Supported:</strong> Strategic budget allocation; expanding high-ROI STEM programs and campus industry alliances.</p>
                </div>
                <div class="metric-card" style="border-left-color: #10b981;">
                    <h4>🎯 Career Advisory Team</h4>
                    <p><strong>Primary Interest:</strong> Proactive identification of at-risk students before final semester.</p>
                    <p><strong>Decision Supported:</strong> Automated early-warning triggers (<50% predicted employment) for mandatory career coaching.</p>
                </div>
                <div class="metric-card" style="border-left-color: #06b6d4;">
                    <h4>📚 Academic Departments</h4>
                    <p><strong>Primary Interest:</strong> Curriculum relevance and graduate marketability.</p>
                    <p><strong>Decision Supported:</strong> Embedding mandatory credit-bearing internships (OR = 1.74) and language fluency centers into core degrees.</p>
                </div>
                <div class="metric-card" style="border-left-color: #f59e0b;">
                    <h4>🎓 Students & Candidates</h4>
                    <p><strong>Primary Interest:</strong> Tuition ROI, job security, starting salary.</p>
                    <p><strong>Decision Supported:</strong> Simulating real-time profile improvements on the Career Early-Warning Dashboard.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
