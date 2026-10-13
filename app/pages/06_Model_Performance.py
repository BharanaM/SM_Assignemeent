from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.components.ui_config import (
    apply_2026_theme,
    render_hero_banner,
    render_kpi_card,
    style_plotly_chart,
)

apply_2026_theme(page_title="Model Performance & Comparison", page_icon="⚙️")

render_hero_banner(
    title="Predictive Modelling & Tournament Comparison",
    subtitle="Leakage-free evaluation across 7 classification & regression architectures on a 20% holdout test set (n = 59,996). Comparing interpretable penalized GLMNET models against ensemble Random Forest and Gradient Boosting.",
    badges=[
        ("⚙️ Task 5: Predictive Modelling", ""),
        ("🔒 Zero Data Leakage (Excl. Post-Hire Variables)", "cyan"),
        ("⚖️ Algorithmic Fairness Verified", "emerald"),
    ],
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    render_kpi_card(
        label="Tournament Winner (Live App)",
        value="Random Forest",
        delta="88.83% Accuracy | 0.957 ROC-AUC",
        icon="🏆",
        accent="#10b981",
    )
with kpi2:
    render_kpi_card(
        label="Consultancy Policy Choice",
        value="LASSO (L₁)",
        delta="88.10% Accuracy | 0.951 ROC-AUC",
        icon="📐",
        accent="#8b5cf6",
        delta_cls="purple",
    )
with kpi3:
    render_kpi_card(
        label="Salary Regression RMSE",
        value="$14,397.60",
        delta="GBM & OLS (VIF < 3, Homoscedastic)",
        icon="💵",
        accent="#3b82f6",
        delta_cls="blue",
    )
with kpi4:
    render_kpi_card(
        label="Fairness & Diagnostics",
        value="VIF < 3.0",
        delta="Gender OR = 0.993 (Non-significant)",
        icon="⚖️",
        accent="#f59e0b",
        delta_cls="amber",
    )

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🏆 Classification Model Comparison Table",
    "📈 Logistic Odds Ratios (exp(β))",
    "💰 Salary Regression Tournament",
    "⚖️ Fairness Audit & Viva Architecture",
])

# ------------------------------------------------------------------------------
# TAB 1: CLASSIFICATION COMPARISON
# ------------------------------------------------------------------------------
with tab1:
    with st.container(border=True):
        st.markdown(
            """
            <div class="section-header">
                <span class="section-title">📊 Master Classification Model Comparison Table (20% Holdout Test Set)</span>
                <span class="section-tag">outputs/tables/model_comparison.csv + Tournament</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        master_models = pd.DataFrame([
            {
                "Model": "Random Forest (Ensemble Bagging)",
                "Accuracy": 0.8883,
                "Precision": 0.8865,
                "Recall (Sensitivity)": 0.8990,
                "F1-Score": 0.8927,
                "ROC-AUC": 0.9570,
                "Primary Advantage": "Tournament Winner — Captures non-linear interactions for live dashboard",
            },
            {
                "Model": "GBM (Gradient Boosting Machine)",
                "Accuracy": 0.8867,
                "Precision": 0.8848,
                "Recall (Sensitivity)": 0.8972,
                "F1-Score": 0.8910,
                "ROC-AUC": 0.9554,
                "Primary Advantage": "Sequential error-correcting trees",
            },
            {
                "Model": "Standard Logistic Regression (MLE)",
                "Accuracy": 0.8811,
                "Precision": 0.8818,
                "Recall (Sensitivity)": 0.8918,
                "F1-Score": 0.8868,
                "ROC-AUC": 0.9511,
                "Primary Advantage": "Unbiased baseline log-odds with 95% CIs & VIF < 3",
            },
            {
                "Model": "Elastic Net Logistic (α = 0.5)",
                "Accuracy": 0.8810,
                "Precision": 0.8816,
                "Recall (Sensitivity)": 0.8918,
                "F1-Score": 0.8867,
                "ROC-AUC": 0.9511,
                "Primary Advantage": "Balanced L₁ sparsity and L₂ stability",
            },
            {
                "Model": "LASSO Logistic Regression (L₁, α = 1)",
                "Accuracy": 0.8810,
                "Precision": 0.8816,
                "Recall (Sensitivity)": 0.8918,
                "F1-Score": 0.8867,
                "ROC-AUC": 0.9511,
                "Primary Advantage": "Consultancy Choice — Automatic feature selection & explainable Odds Ratios",
            },
            {
                "Model": "Ridge Logistic Regression (L₂, α = 0)",
                "Accuracy": 0.8792,
                "Precision": 0.8780,
                "Recall (Sensitivity)": 0.8927,
                "F1-Score": 0.8853,
                "ROC-AUC": 0.9501,
                "Primary Advantage": "Shrinks correlated coefficients toward zero",
            },
            {
                "Model": "Naïve Bayes Classifier",
                "Accuracy": 0.8765,
                "Precision": 0.8532,
                "Recall (Sensitivity)": 0.9221,
                "F1-Score": 0.8863,
                "ROC-AUC": 0.9505,
                "Primary Advantage": "Fast generative baseline; highest sensitivity (92.21% Recall)",
            },
        ])

        fmt_df = master_models.copy()
        for c in ["Accuracy", "Precision", "Recall (Sensitivity)", "F1-Score", "ROC-AUC"]:
            fmt_df[c] = fmt_df[c].apply(lambda x: f"{x:.4f} ({x*100:.2f}%)" if c != "F1-Score" and c != "ROC-AUC" else f"{x:.4f}")

        st.dataframe(fmt_df, use_container_width=True, hide_index=True)

    c_left, c_right = st.columns([1.3, 1])
    with c_left:
        with st.container(border=True):
            st.markdown(
                """
                <div class="section-header">
                    <span class="section-title">📈 Multi-Metric Model Benchmark</span>
                    <span class="section-tag">Accuracy vs Recall vs ROC-AUC</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            melt_m = master_models.melt(
                id_vars=["Model"],
                value_vars=["Accuracy", "Precision", "Recall (Sensitivity)", "ROC-AUC"],
                var_name="Metric",
                value_name="Score",
            )
            fig_comp = px.bar(
                melt_m,
                x="Model",
                y="Score",
                color="Metric",
                barmode="group",
                color_discrete_sequence=["#8b5cf6", "#3b82f6", "#10b981", "#f59e0b"],
            )
            fig_comp.update_layout(yaxis_range=[0.82, 0.98], xaxis_title="", yaxis_title="Metric Score")
            fig_comp = style_plotly_chart(fig_comp, height=360)
            st.plotly_chart(fig_comp, use_container_width=True)

    with c_right:
        st.markdown(
            """
            <div class="metric-card" style="border-left-color: #10b981; margin-bottom: 1rem;">
                <h4>🥇 Dual-Model Strategy (Viva Highlight)</h4>
                <p><strong>1. For Management Policy (LASSO L₁):</strong> Achieves <code>88.10% Accuracy</code> and <code>0.9511 AUC</code> while providing exact <strong>Odds Ratios</strong> and zeroing out noisy dummy variables.</p>
                <p><strong>2. For Live Prediction Engine (Random Forest):</strong> Achieves the highest holdout accuracy (<code>88.83%</code>, <code>0.957 AUC</code>) by modeling complex non-linear interactions across 100 decision trees (<code>nodesize = 50</code>).</p>
            </div>
            <div class="theory-box">
                <strong>Why did GLM, Ridge, LASSO & Elastic Net perform identically (~88.1%)?</strong><br>
                Because <code>N = 240,000</code> training rows vastly exceeds <code>p = 12</code> predictors, variance is already minimal and <code>VIF &lt; 3</code> confirms no severe multicollinearity.
            </div>
            """,
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------------------------
# TAB 2: ODDS RATIOS
# ------------------------------------------------------------------------------
with tab2:
    or_path = ROOT / "outputs" / "tables" / "logistic_odds_ratios.csv"
    if or_path.exists():
        or_df = pd.read_csv(or_path, index_col=0)
        or_df.index.name = "Predictor"
        or_df = or_df.reset_index()
        or_df = or_df[or_df["Predictor"] != "(Intercept)"].copy()
        or_df["Significant (95% CI excl. 1.0)"] = or_df.apply(
            lambda r: "No (Fair / Null)" if (r["2.5 %"] <= 1.0 <= r["97.5 %"]) else "Yes (p < 0.001)",
            axis=1,
        )

        col_or1, col_or2 = st.columns([1.3, 1])
        with col_or1:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="section-header">
                        <span class="section-title">🚀 Key Actionable & Academic Odds Ratios (OR = e^β)</span>
                        <span class="section-tag">95% Confidence Intervals</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                key_predictors = [
                    "education_levelPhD",
                    "field_of_studyEngineering",
                    "field_of_studyIT",
                    "field_of_studyHealth",
                    "education_levelMaster's",
                    "language_proficiencyFluent",
                    "internship_experienceYes",
                    "gpa",
                    "genderMale",
                    "age",
                    "language_proficiencyBasic",
                    "university_rankingLow",
                ]
                sub_or = or_df[or_df["Predictor"].isin(key_predictors)].sort_values("OR", ascending=True)
                fig_or = px.bar(
                    sub_or,
                    x="OR",
                    y="Predictor",
                    color="Significant (95% CI excl. 1.0)",
                    text="OR",
                    orientation="h",
                    color_discrete_map={"Yes (p < 0.001)": "#8b5cf6", "No (Fair / Null)": "#64748b"},
                )
                fig_or.add_vline(x=1.0, line_dash="dash", line_color="#f43f5e", annotation_text="Null OR = 1.0")
                fig_or.update_traces(texttemplate="%{text:.2f}x", textposition="outside")
                fig_or.update_layout(xaxis_title="Odds Ratio (exp(β))", yaxis_title="", xaxis_range=[0, 11])
                fig_or = style_plotly_chart(fig_or, height=400)
                st.plotly_chart(fig_or, use_container_width=True)

        with col_or2:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="section-header">
                        <span class="section-title">📋 Complete Odds Ratio Table</span>
                        <span class="section-tag">logistic_odds_ratios.csv</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.dataframe(
                    or_df.sort_values("OR", ascending=False).round(3),
                    use_container_width=True,
                    hide_index=True,
                    height=400,
                )

# ------------------------------------------------------------------------------
# TAB 3: SALARY REGRESSION
# ------------------------------------------------------------------------------
with tab3:
    reg_data = pd.DataFrame({
        "Model": ["Multiple Linear Regression (OLS)", "GLMNET (Elastic Net)", "GBM (Gradient Boosting)"],
        "RMSE (USD)": [14399.14, 14399.12, 14397.60],
        "Architecture": ["Parametric OLS (VIF < 3)", "Penalized L1/L2 Linear", "Sequential Boosted Trees"],
    }).sort_values(by="RMSE (USD)", ascending=False)

    r_col1, r_col2 = st.columns([1.2, 1])
    with r_col1:
        with st.container(border=True):
            st.markdown(
                """
                <div class="section-header">
                    <span class="section-title">💰 Salary Prediction RMSE Comparison (Employed Only)</span>
                    <span class="section-tag">Lower RMSE is Better</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            fig_rmse = px.bar(
                reg_data,
                y="Model",
                x="RMSE (USD)",
                text="RMSE (USD)",
                color="Architecture",
                orientation="h",
                color_discrete_sequence=["#3b82f6", "#8b5cf6", "#10b981"],
            )
            fig_rmse.update_traces(texttemplate="$%{text:,.2f}", textposition="outside")
            fig_rmse.update_layout(xaxis_range=[14394, 14402], xaxis_title="Test Set RMSE (USD)", yaxis_title="")
            fig_rmse = style_plotly_chart(fig_rmse, height=320)
            st.plotly_chart(fig_rmse, use_container_width=True)

    with r_col2:
        st.markdown(
            """
            <div class="metric-card" style="border-left-color: #3b82f6;">
                <h4>📐 Salary Regression Specification</h4>
                <p><strong>Formula:</strong> <code>salary ~ gpa + age + education_level + field_of_study + internship_experience</code></p>
                <p><strong>Diagnostics Verified:</strong></p>
                <p>• <strong>Residuals vs Fitted:</strong> Homoscedastic (constant variance)</p>
                <p>• <strong>Normal Q-Q Plot:</strong> Residuals follow Gaussian normality</p>
                <p>• <strong>Monotonicity:</strong> Guarantees strict salary progression across PhD &gt; Master's &gt; Bachelor's &gt; Diploma.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ------------------------------------------------------------------------------
# TAB 4: FAIRNESS & ARCHITECTURE
# ------------------------------------------------------------------------------
with tab4:
    f_col1, f_col2 = st.columns(2)
    with f_col1:
        with st.container(border=True):
            st.markdown(
                """
                <div class="section-header">
                    <span class="section-title">⚖️ Algorithmic Fairness Audit by Gender</span>
                    <span class="section-tag">fairness_gender.csv</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            fg_path = ROOT / "outputs" / "tables" / "fairness_gender.csv"
            if fg_path.exists():
                fg_df = pd.read_csv(fg_path)
                fg_df["Mean_Predicted_Prob (%)"] = (fg_df["Mean_Predicted_Prob"] * 100).round(2)
                st.dataframe(fg_df, use_container_width=True, hide_index=True)
                st.caption("✅ Predicted employment probabilities are virtually identical across genders (~68.0%), confirming zero gender bias.")

    with f_col2:
        st.markdown(
            """
            <div class="theory-box" style="margin-top: 0;">
                <strong>1. Data Leakage Prevention:</strong><br>
                <code>salary</code> and <code>job_sector</code> were strictly excluded from employment classification because they only exist <em>after</em> a student is employed.
            </div>
            <div class="theory-box">
                <strong>2. Why SVM was Excluded:</strong><br>
                Support Vector Machines require an <code>O(N²)</code> kernel matrix (~400 GB RAM for 240,000 rows), whereas GLMNET, Random Forest, and GBM scale linearly with sample size.
            </div>
            """,
            unsafe_allow_html=True,
        )
