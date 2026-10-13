import streamlit as st
from app.components.ui_config import (
    apply_2026_theme,
    render_hero_banner,
    render_kpi_card,
)

apply_2026_theme(page_title="Experimental Design, Time Series & Innovation", page_icon="🚀")

render_hero_banner(
    title="Experimental Design, Time Series & Strategic Roadmap",
    subtitle="Extending cross-sectional statistical modeling into causal inference (Task 6 RCBD), macro cohort forecasting (Task 9 ARIMA/SARIMA), and institutional deployment governance (Tasks 10–12).",
    badges=[
        ("🧪 Task 6: RCBD Experimental Design", ""),
        ("📈 Task 9: ARIMA / SARIMA Forecasting", "cyan"),
        ("🏛️ Tasks 10–12: Governance & Ethics", "emerald"),
    ],
)

k1, k2, k3, k4 = st.columns(4)
with k1:
    render_kpi_card("Causal Design", "RCBD", "Blocks on GPA & Degree Tier", "🧪", "#8b5cf6", "purple")
with k2:
    render_kpi_card("Macro Forecasting", "SARIMA", "12–18 Month Cohort Horizon", "📈", "#3b82f6", "blue")
with k3:
    render_kpi_card("Privacy Standard", "FERPA / GDPR", "PII & Demographic Stripping", "🔒", "#10b981")
with k4:
    render_kpi_card("Model Retraining", "Annual Cycle", "Mitigates concept & market drift", "🔄", "#f59e0b", "amber")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="metric-card" style="border-left-color: #8b5cf6; margin-bottom: 1.2rem;">
            <h3>🧪 Task 6: Randomized Complete Block Design (RCBD)</h3>
            <p><strong>Why Observational Data Cannot Prove Causality:</strong> Our survey dataset is observational—high-achieving students may self-select into internships.</p>
            <p><strong>Proposed RCBD Protocol:</strong></p>
            <p>• <strong>Blocking Factors:</strong> Block students into homogeneous strata based on <code>GPA Tier</code> and <code>Education Level</code> to eliminate confounding variance.</p>
            <p>• <strong>Treatment Assignment:</strong> Randomly assign students within each block to <em>Standard Career Advising (Control)</em> vs. <em>Mandatory Credit-Bearing Industry Internship (Treatment)</em>.</p>
            <p>• <strong>Response Metrics:</strong> 6-month post-graduation employment rate and starting salary.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="metric-card" style="border-left-color: #10b981;">
            <h3>🏛️ Tasks 11 & 12: Expert Validation & Strategic Policy</h3>
            <p><strong>Director of Career Services Feedback:</strong> Emphasized that career advisors cannot alter a student's demographic background or university tier, so operational triggers must prioritize <strong>actionable levers</strong>.</p>
            <p><strong>Top 3 Institutional Recommendations:</strong></p>
            <p>1. <strong>Mandate Credit-Bearing Internships:</strong> Increases employment odds by <code>74.1% (OR = 1.74)</code> and boosts starting pay (<code>Cohen's d = 0.54</code>).</p>
            <p>2. <strong>Deploy Sophomore Early-Warning Screening:</strong> Flag students below <code>50%</code> predicted employability for mandatory coaching.</p>
            <p>3. <strong>Expand Communication & Fluency Centers:</strong> Fluency yields <code>OR = 2.16</code> and <code>Cramer's V = 0.251</code>.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="metric-card" style="border-left-color: #06b6d4; margin-bottom: 1.2rem;">
            <h3>📈 Task 9: Time Series Forecasting (ARIMA / SARIMA)</h3>
            <p><strong>Why Cross-Sectional Data Cannot Fit ARIMA Directly:</strong> Our 299,984 records represent a static cross-sectional snapshot lacking longitudinal timestamps (graduation month/quarter).</p>
            <p><strong>Longitudinal Cohort Extension:</strong> By tracking quarterly graduate employment rates over time, universities can deploy <strong>Seasonal ARIMA (SARIMA)</strong> to:</p>
            <p>• <strong>Forecast Graduate Unemployment:</strong> Project macro hiring demand 12–18 months ahead.</p>
            <p>• <strong>Capture Seasonal Hiring Surges:</strong> Align campus career fairs with Q3/September recruitment peaks.</p>
            <p>• <strong>Honest Limitations:</strong> Vulnerable to structural macroeconomic breaks (e.g., pandemic shocks or tech hiring freezes) and short historical series.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="metric-card" style="border-left-color: #f59e0b;">
            <h3>⚖️ Ethical Governance, Cost & Maintenance</h3>
            <p><strong>Algorithmic Fairness:</strong> Protected attributes (<code>gender</code>, <code>country_of_origin</code>) are audited annually and stripped from operational student scoring to prevent bias.</p>
            <p><strong>Operational Budget:</strong> Cloud hosting (~$1,200/yr) + annual model recalibration using new graduating cohort outcomes to prevent model drift.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
