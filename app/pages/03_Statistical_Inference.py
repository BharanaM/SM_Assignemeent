from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px

APP_DIR = Path(__file__).resolve().parents[1]
ROOT = APP_DIR.parent
for p in [str(ROOT), str(APP_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from components.ui_config import (
        apply_2026_theme,
        render_hero_banner,
        render_kpi_card,
        style_plotly_chart,
    )
except Exception:
    from app.components.ui_config import (
        apply_2026_theme,
        render_hero_banner,
        render_kpi_card,
        style_plotly_chart,
    )

apply_2026_theme(page_title="Statistical Inference", page_icon="📈")

render_hero_banner(
    title="Statistical Inference & Hypothesis Testing Suite",
    subtitle="Parametric and non-parametric hypothesis testing across N = 299,984 graduates, fortified with Benjamini-Hochberg False Discovery Rate (FDR) correction and standardized Effect Size quantification.",
    badges=[
        ("📈 Task 4: Statistical Inference", ""),
        ("🛡️ Benjamini-Hochberg FDR Applied", "cyan"),
        ("⚖️ Parametric + Non-Parametric Fallbacks", "emerald"),
    ],
)

results_path = ROOT / "outputs" / "tables" / "inference_results.csv"

if results_path.exists():
    df_results = pd.read_csv(results_path)

    # Top KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card(
            label="Hypotheses Evaluated",
            value=f"{len(df_results)} Core Tests",
            delta="+3 Phase-3 Variance/ANOVA Checks",
            icon="🧪",
            accent="#8b5cf6",
            delta_cls="purple",
        )
    with c2:
        render_kpi_card(
            label="BH-Adjusted Significance",
            value=f"{len(df_results[df_results['Significant'] == 'Yes'])} / {len(df_results)}",
            delta="All p_adj < 0.0001 (FDR α = 0.05)",
            icon="✅",
            accent="#10b981",
        )
    with c3:
        render_kpi_card(
            label="Top Salary Driver",
            value="Education Level",
            delta="Eta-squared η² = 0.458 (Large)",
            icon="🎓",
            accent="#3b82f6",
            delta_cls="blue",
        )
    with c4:
        render_kpi_card(
            label="Top Employment Driver",
            value="Internship & Ranking",
            delta="Cohen's h = 0.488 | Cramer's V = 0.374",
            icon="🚀",
            accent="#f59e0b",
            delta_cls="amber",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "📊 Hypothesis & p-Value Table",
        "📐 Effect Size Comparison Chart",
        "🧠 Viva Methodology & Assumption Checks",
    ])

    with tab1:
        with st.container(border=True):
            st.markdown(
                """
                <div class="section-header">
                    <span class="section-title">🧪 Master Statistical Inference & Adjusted p-Value Table</span>
                    <span class="section-tag">R/02_statistical_inference.R</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            display_df = df_results.copy()
            display_df["P_Value"] = display_df["P_Value"].apply(
                lambda x: "< 0.0001" if pd.notnull(x) and float(x) < 0.0001 else f"{float(x):.4e}"
            )
            display_df["Adjusted_P_Value"] = display_df["Adjusted_P_Value"].apply(
                lambda x: "< 0.0001" if pd.notnull(x) and float(x) < 0.0001 else f"{float(x):.4e}"
            )
            display_df["Effect_Size_Value"] = display_df["Effect_Size_Value"].apply(
                lambda x: "Heteroscedastic" if pd.isna(x) else f"{float(x):.3f}"
            )

            display_df = display_df.rename(
                columns={
                    "Test_Name": "Hypothesis Test",
                    "H0": "Null Hypothesis (H₀)",
                    "H1": "Alternative Hypothesis (H₁)",
                    "Test_Used": "Statistical Test",
                    "P_Value": "Raw p-Value",
                    "Adjusted_P_Value": "BH-Adjusted p-Value",
                    "Effect_Size_Metric": "Effect Metric",
                    "Effect_Size_Value": "Effect Size",
                    "Practical_Meaning": "Practical / Business Meaning",
                    "Significant": "Reject H₀?",
                }
            )

            st.dataframe(display_df, use_container_width=True, hide_index=True, height=320)
            st.caption(
                "💡 **Viva Note:** Because N = 299,984 is very large, standard errors (SE = s/√n) are tiny and raw p-values underflow to < 2.2e-16 (< 0.0001). Therefore, **Effect Size** (Cohen's d, Cohen's h, η², Cramer's V) is essential to rank practical importance!"
            )

    with tab2:
        col_left, col_right = st.columns([1.35, 1])

        with col_left:
            with st.container(border=True):
                st.markdown(
                    """
                    <div class="section-header">
                        <span class="section-title">📐 Standardized Effect Size Magnitude by Test</span>
                        <span class="section-tag">Practical Significance Ranking</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                eff_df = df_results.dropna(subset=["Effect_Size_Value"]).copy()
                eff_df["Effect_Size_Value"] = pd.to_numeric(eff_df["Effect_Size_Value"])
                eff_df = eff_df.sort_values("Effect_Size_Value", ascending=True)

                fig_eff = px.bar(
                    eff_df,
                    x="Effect_Size_Value",
                    y="Test_Name",
                    color="Effect_Size_Metric",
                    text="Effect_Size_Value",
                    orientation="h",
                    color_discrete_sequence=["#8b5cf6", "#10b981", "#3b82f6", "#f59e0b"],
                )
                fig_eff.update_traces(texttemplate="%{text:.3f}", textposition="outside")
                fig_eff.update_layout(
                    xaxis_title="Effect Size Magnitude",
                    yaxis_title="",
                    xaxis_range=[0, 0.62],
                )
                fig_eff = style_plotly_chart(fig_eff, height=360)
                st.plotly_chart(fig_eff, use_container_width=True)

        with col_right:
            st.markdown(
                """
                <div class="metric-card" style="border-left-color: #8b5cf6; margin-bottom: 1rem;">
                    <h4>📏 Effect Size Benchmarks</h4>
                    <p><strong>• Cohen's d (t-test):</strong> <code>0.538</code> (Medium positive salary boost from Internships)</p>
                    <p><strong>• Cohen's h (2-Prop Z-test):</strong> <code>0.488</code> (Strong employment rate jump: 71.6% vs 57.6%)</p>
                    <p><strong>• Eta-squared η² (ANOVA):</strong> <code>0.458</code> (Large effect — 45.8% of salary variance explained by Degree Level)</p>
                    <p><strong>• Cramer's V (Chi-Square):</strong> Ranking (<code>0.374</code>) &gt; Language Fluency (<code>0.251</code>) &gt; Field of Study (<code>0.119</code>)</p>
                </div>
                <div class="theory-box">
                    <strong>Why Effect Size Matters in Viva:</strong><br>
                    With <code>N = 299,984</code>, every test achieves <code>p &lt; 0.0001</code>. Reporting effect sizes proves whether a statistically significant finding is also <em>practically meaningful</em> for university resource allocation.
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab3:
        st.markdown("### 🔬 Parametric Assumptions, Non-Parametric Fallbacks & Phase-3 Diagnostics")
        c_a, c_b, c_c = st.columns(3)
        with c_a:
            st.markdown(
                """
                <div class="metric-card" style="border-left-color: #3b82f6;">
                    <h4>1. Homogeneity of Variance</h4>
                    <p><strong>Test:</strong> Levene's Test across Education Levels</p>
                    <p><strong>Result:</strong> <code>p = 1.96 × 10⁻¹²⁹</code> (Reject H₀)</p>
                    <p><strong>Action Taken:</strong> Because PhD salaries have higher variance than Diplomas, we paired One-Way ANOVA with the non-parametric <strong>Kruskal-Wallis test</strong> and Welch's t-test with <strong>Mann-Whitney U</strong>.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c_b:
            st.markdown(
                """
                <div class="metric-card" style="border-left-color: #10b981;">
                    <h4>2. Structural Missingness Rule</h4>
                    <p><strong>Scope:</strong> Salary Tests (Tests 1, 3, 4)</p>
                    <p><strong>Cohort:</strong> Employed Graduates Only (<code>n = 204,101</code>)</p>
                    <p><strong>Rationale:</strong> Unemployed graduates have <code>$0 / NA</code> salary structurally. Filtering to employed graduates prevents confounding employment rate with starting pay.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with c_c:
            st.markdown(
                """
                <div class="metric-card" style="border-left-color: #f59e0b;">
                    <h4>3. Multiple Testing Correction</h4>
                    <p><strong>Method:</strong> Benjamini-Hochberg (BH) FDR</p>
                    <p><strong>Formula:</strong> Controls expected False Discovery Rate at <code>α = 0.05</code> across simultaneous family of tests.</p>
                    <p><strong>Outcome:</strong> All 7 core hypotheses and 3 Phase-3 tests remain highly significant after BH adjustment.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.error("Statistical results file not found at `outputs/tables/inference_results.csv`.")
