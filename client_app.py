from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import base64
import subprocess
import json
import platform
import shutil

# Root configuration
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.config import PROCESSED_DATA
from app.components.model_ui import employment_form

from app.components.ui_config import apply_2026_theme

# Apply the main project theme to get all the nice glassmorphism and fonts
apply_2026_theme(page_title="Employment & Salary Prediction Portal", page_icon="🎓")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_dark_background(png_file):
    try:
        bin_str = get_base64_of_bin_file(png_file)
        # We add a dark linear gradient overlay over the image so white text is highly readable
        page_bg_img = f'''
        <style>
        .stApp {{
            background-image: 
                linear-gradient(to bottom, rgba(2, 6, 23, 0.8), rgba(2, 6, 23, 0.9)),
                url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        '''
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except Exception as e:
        pass

# Apply the professional background image with dark overlay
bg_path = ROOT / "res" / "background.jpg"
if bg_path.exists():
    set_dark_background(bg_path)

st.markdown("<h1 style='text-align: center;'>🎓 Graduate Employment & Salary Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2em; color: #cbd5e1;'>Welcome to our dual-engine predictive portal. Evaluate candidate profiles to forecast both employment probability and expected starting salary.</p>", unsafe_allow_html=True)
st.markdown("---")

df = pd.read_csv(PROCESSED_DATA)

with st.container():
    st.subheader("📝 Candidate Profile Input")
    inputs = employment_form(df)
    
st.divider()

if st.button("🚀 Calculate Employment & Salary Forecast", type="primary", use_container_width=True):
    with st.spinner("Analyzing candidate profile against historical data..."):
        # Cross-platform Rscript path
        if platform.system() == "Windows":
            default_path = r"E:\R-4.6.1\bin\Rscript.exe"
            RSCRIPT_PATH = default_path if Path(default_path).exists() else (shutil.which("Rscript") or "Rscript")
        else:
            RSCRIPT_PATH = "Rscript"
        
        script_path = str(ROOT / "R" / "predict_new.R")
        inputs_json = inputs.to_json(orient='records')
        
        try:
            result = subprocess.run(
                [RSCRIPT_PATH, script_path, inputs_json], 
                capture_output=True, text=True, check=True
            )
            
            lines = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            r_output = json.loads(lines[-1])
            emp_prob = float(r_output["employed_probability"])
            predicted_salary = float(r_output.get("predicted_salary", 0.0))
        except FileNotFoundError:
            st.error("⚠️ **Could not find Rscript!** Please configure the correct path in `client_app.py`.")
            st.stop()
        except subprocess.CalledProcessError as e:
            st.error(f"Error connecting to R backend: {e}")
            if e.stderr:
                st.error(f"Details: {e.stderr}")
            st.stop()
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            st.stop()
        
        st.markdown("### 🎯 Prediction & Forecast Results")
        st.markdown("<hr style='margin-top: 0; margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
        
        # Historical cohort benchmarks
        employed_df = df[df["employment_status"] == "Employed"]
        overall_median_salary = float(employed_df["salary"].median())
        cand_field = str(inputs["field_of_study"].iloc[0])
        cand_degree = str(inputs["education_level"].iloc[0])
        cand_gpa = float(inputs["gpa"].iloc[0])
        cand_intern = str(inputs["internship_experience"].iloc[0])
        
        field_salaries = employed_df[employed_df["field_of_study"] == cand_field]["salary"]
        field_median_salary = float(field_salaries.median()) if not field_salaries.empty else overall_median_salary
        
        degree_salaries = employed_df[employed_df["education_level"] == cand_degree]["salary"]
        degree_median_salary = float(degree_salaries.median()) if not degree_salaries.empty else overall_median_salary

        # 4 High-level metric KPI cards
        m1, m2, m3, m4 = st.columns(4)
        prob_pct = emp_prob * 100
        salary_diff = predicted_salary - overall_median_salary
        salary_diff_str = f"{'+' if salary_diff >= 0 else ''}${salary_diff:,.0f} vs Market Median"

        if predicted_salary >= 104500:
            bracket = "Top Tier (Top 25%)"
        elif predicted_salary >= 92000:
            bracket = "Upper-Mid Bracket"
        elif predicted_salary >= 79000:
            bracket = "Mid-Range Bracket"
        else:
            bracket = "Entry Bracket"

        with m1:
            st.metric(
                label="Employment Probability",
                value=f"{prob_pct:.1f}%",
                delta="Strong Outlook" if emp_prob >= 0.5 else "Targeted Support",
                delta_color="normal" if emp_prob >= 0.5 else "inverse"
            )

        with m2:
            st.metric(
                label="Estimated Starting Salary",
                value=f"${predicted_salary:,.0f}",
                delta=salary_diff_str,
                delta_color="normal" if salary_diff >= 0 else "inverse"
            )

        with m3:
            st.metric(
                label="Monthly Equivalent",
                value=f"${predicted_salary / 12:,.0f}",
                delta="Annualized estimate"
            )

        with m4:
            st.metric(
                label="Compensation Tier",
                value=bracket,
                delta=f"{cand_field} • {cand_degree}"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Tabbed deep-dive
        tab1, tab2 = st.tabs(["🔮 Employment Probability Analysis", "💰 Salary Forecast & Benchmarking"])

        with tab1:
            col1, col2 = st.columns([1, 1.2])
            with col1:
                st.markdown("<br>", unsafe_allow_html=True)
                if emp_prob >= 0.5:
                    st.success("### 🎉 Highly Competitive Candidate")
                    st.markdown(
                        "**Strategic Assessment:** Candidate profile exhibits robust alignment with employer requirements.\n\n"
                        "**Key Drivers:** High academic achievement (GPA), field demand, and background credentials "
                        "consistently indicate a streamlined transition into full-time roles.\n\n"
                        "**Recommendation:** Expedite candidate through recruitment screening and offer competitive terms."
                    )
                else:
                    st.error("### ⚠️ Needs Targeted Support")
                    st.markdown(
                        "**Strategic Assessment:** Candidate profile reflects competitive headwinds under current job market conditions.\n\n"
                        "**Key Drivers:** Attributes indicate potential placement friction. Targeted upskilling, portfolio projects, "
                        "and internship bridging will substantially enhance competitiveness.\n\n"
                        "**Recommendation:** Provide proactive career counseling, resume optimization, and targeted internship pathways."
                    )

                with st.expander("🔍 View Candidate Input Summary", expanded=False):
                    summary_cols = st.columns(2)
                    with summary_cols[0]:
                        st.markdown(f"- **Field:** {cand_field}")
                        st.markdown(f"- **Degree:** {cand_degree}")
                        st.markdown(f"- **GPA:** {cand_gpa:.2f}")
                    with summary_cols[1]:
                        st.markdown(f"- **Internship:** {cand_intern}")
                        st.markdown(f"- **Origin:** {inputs['country_of_origin'].iloc[0]}")
                        st.markdown(f"- **Visa:** {inputs['visa_type'].iloc[0]}")

            with col2:
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = emp_prob * 100,
                    title = {'text': "Employment Probability", 'font': {'size': 20, 'color': '#f8fafc'}},
                    number = {'suffix': "%", 'font': {'size': 36, 'color': '#f8fafc'}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                        'bar': {'color': "#8b5cf6" if emp_prob >= 0.5 else "#f43f5e"},
                        'bgcolor': "rgba(30, 41, 59, 0.5)",
                        'borderwidth': 2,
                        'bordercolor': "rgba(255,255,255,0.1)",
                        'steps': [
                            {'range': [0, 50], 'color': 'rgba(244, 63, 94, 0.2)'},
                            {'range': [50, 100], 'color': 'rgba(139, 92, 246, 0.2)'}],
                    }
                ))
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=260, margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            sal_col1, sal_col2 = st.columns([1, 1.2])
            with sal_col1:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("#### 💵 Salary Benchmark Analysis")
                diff_field = predicted_salary - field_median_salary
                diff_deg = predicted_salary - degree_median_salary
                
                low_band = predicted_salary * 0.93
                high_band = predicted_salary * 1.07

                st.markdown(
                    f"- **Expected Base Range:** **${low_band:,.0f} – ${high_band:,.0f}** *(±7% model confidence interval)*\n"
                    f"- **Field Peer Baseline ({cand_field}):** **{'+' if diff_field >= 0 else ''}${diff_field:,.0f}** vs median (${field_median_salary:,.0f})\n"
                    f"- **Degree Peer Baseline ({cand_degree}):** **{'+' if diff_deg >= 0 else ''}${diff_deg:,.0f}** vs median (${degree_median_salary:,.0f})\n"
                    f"- **Overall Market Median:** **{'+' if salary_diff >= 0 else ''}${salary_diff:,.0f}** vs benchmark (${overall_median_salary:,.0f})"
                )

                if emp_prob >= 0.5:
                    st.info(
                        "💡 **Compensation Outlook:** The candidate holds solid credentials justifying compensation packages "
                        f"in the **${predicted_salary:,.0f}** range, placing them squarely in a competitive negotiating position."
                    )
                else:
                    st.warning(
                        f"💡 **Employability Context:** Although placement probability is currently below 50%, "
                        f"the candidate's structural earning potential once employed is evaluated at **${predicted_salary:,.0f}**. "
                        "Securing an entry internship or certification will help realize this market valuation."
                    )

            with sal_col2:
                # Salary Meter Gauge
                salary_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=predicted_salary,
                    title={'text': "Annual Salary Forecast (USD)", 'font': {'size': 20, 'color': '#f8fafc'}},
                    number={'prefix': "$", 'valueformat': ",.0f", 'font': {'size': 34, 'color': '#38bdf8'}},
                    gauge={
                        'axis': {'range': [40000, 145000], 'tickwidth': 1, 'tickcolor': "white", 'tickformat': "$,.0f"},
                        'bar': {'color': "#38bdf8"},
                        'bgcolor': "rgba(30, 41, 59, 0.5)",
                        'borderwidth': 2,
                        'bordercolor': "rgba(255,255,255,0.1)",
                        'steps': [
                            {'range': [40000, 79000], 'color': 'rgba(148, 163, 184, 0.15)'},
                            {'range': [79000, 104000], 'color': 'rgba(59, 130, 246, 0.2)'},
                            {'range': [104000, 145000], 'color': 'rgba(16, 185, 129, 0.25)'}
                        ],
                        'threshold': {
                            'line': {'color': "#f59e0b", 'width': 3},
                            'thickness': 0.75,
                            'value': overall_median_salary
                        }
                    }
                ))
                salary_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=240, margin=dict(l=10, r=10, t=40, b=10))
                st.plotly_chart(salary_gauge, use_container_width=True)

            # Horizontal benchmark comparison chart
            benchmarks_df = pd.DataFrame({
                "Benchmark": [
                    "Market Median", 
                    f"{cand_field} Median", 
                    f"{cand_degree} Median", 
                    "Candidate Forecast"
                ],
                "Salary": [
                    overall_median_salary, 
                    field_median_salary, 
                    degree_median_salary, 
                    predicted_salary
                ]
            })
            fig_bar = px.bar(
                benchmarks_df,
                x="Salary",
                y="Benchmark",
                orientation="h",
                text="Salary",
                color="Benchmark",
                color_discrete_map={
                    "Market Median": "#64748b",
                    f"{cand_field} Median": "#818cf8",
                    f"{cand_degree} Median": "#a855f7",
                    "Candidate Forecast": "#38bdf8"
                }
            )
            fig_bar.update_traces(
                texttemplate='$%{text:,.0f}', 
                textposition='inside',
                insidetextfont=dict(color='white', size=13)
            )
            fig_bar.update_layout(
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=220,
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)", title="Annual Salary (USD)", tickformat="$,.0f"),
                yaxis=dict(title="")
            )
            st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.info("⚠️ **Disclaimer:** This is a model-based estimate generated from historical associations. It should not be used as an absolute individual employability label.")
