import streamlit as st

from app.components.ui_config import apply_2026_theme
apply_2026_theme(page_title="Time Series & Innovation", page_icon="🚀")



st.title("🚀 Time Series & Innovation Proposal (Tasks 9 & 10)")
st.markdown("Exploring advanced forecasting methodologies and translating predictive analytics into a tangible business solution.")

with st.expander("📈 Time Series Analysis (Task 9: Discussion)", expanded=True):
    st.markdown("""
    **Overview:** Time series analysis tracks data sequentially over time to identify underlying structures such as **trend** and **seasonality**. Autoregressive Integrated Moving Average (ARIMA) models leverage these past patterns to forecast future values.
    
    **Data Limitations:** Our current dataset is strictly **cross-sectional**, providing a static snapshot. To perform time series forecasting, we are missing longitudinal timestamps (graduation year/month) and continuous cohort data tracking employment over consecutive quarters.
    
    **Forecasting Examples & Applications (If data were available):**
    * **Forecast Graduate Unemployment Rates:** Predicting macro-level hiring trends 12-18 months in advance using ARIMA.
    * **Identify Seasonal Hiring Peaks:** Recognizing reliable post-graduation hiring spikes (e.g., September surges) to perfectly time career fairs.
    * **Early Warning Systems:** Detecting early signs of macroeconomic downturns in specific sectors before they impact the broader student body.
    
    **Limits of Time Series:** Highly vulnerable to **structural breaks** (e.g., the COVID-19 pandemic completely invalidating historical trends), extremely **short data series**, and unpredictable **external shocks**.
    """)

with st.expander("💡 Industry Innovation Proposal (Task 10)", expanded=True):
    st.markdown("""
    ### Proposed Solution: Streamlit "Career Early-Warning Dashboard"
    **Business Need:** University career services struggle with resource allocation, often providing generic advice to the masses rather than targeted interventions for students highly likely to face long-term unemployment.
    
    **Proposed Solution:** A live, interactive Streamlit employment-probability dashboard functioning as an early-warning and career-decision support tool. By inputting a student's profile, the dashboard outputs their live probability of securing employment using our penalized LASSO model.
    
    ### Organizational Impact, Benefits, and Challenges
    * **Benefits:** Transforms career services from a reactive counseling center into a proactive, data-driven intervention unit.
    * **Challenges:** Ensuring user adoption among non-technical staff and preventing the stigmatization of "at-risk" students.
    * **Resources & Costs:** Requires a dedicated Data Scientist for model retraining ($80k-$100k/year) and cloud hosting for the Streamlit app.
    * **Data Privacy:** Strict adherence to FERPA/GDPR is required. Models must strip PII and sensitive demographic data (e.g., gender, country of origin) to prevent algorithmic discrimination.
    * **Maintenance & Feedback Loop:** The model requires annual retraining using the latest cohort's post-graduation data to prevent model drift as market conditions evolve.
    """)
