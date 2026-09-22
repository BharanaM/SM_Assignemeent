from pathlib import Path
import sys
import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

st.set_page_config(page_title="Statistical Inference", page_icon="📈", layout="wide")

# Custom CSS for a beautiful, premium UI
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #1E3A8A; font-weight: 800; }
    h2, h3 { color: #2563EB; }
    .metric-card {
        background-color: #F8FAFC;
        border-left: 5px solid #3B82F6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-value { font-size: 2.5rem; font-weight: 700; color: #1E3A8A; }
    .metric-label { font-size: 1rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Statistical Inference Results")
st.markdown("This section details the rigorous statistical tests conducted to measure the strength and significance of relationships between graduate attributes and employment outcomes.")
st.info("💡 **Methodology Note:** All tests utilize advanced techniques including multiple testing corrections (Benjamini-Hochberg FDR) and effect size measurements (Cohen's d, Cramer's V) to ensure high academic rigor.")

results_path = Path(__file__).resolve().parents[2] / "res" / "all_results.csv"

if results_path.exists():
    df_results = pd.read_csv(results_path)
    
    # ---------------------------------------------------------
    # TOP KPI METRIC CARDS
    # ---------------------------------------------------------
    col1, col2, col3 = st.columns(3)
    
    total_tests = len(df_results)
    significant_tests = len(df_results[df_results['Significant'] == 'Yes'])
    
    # Find the feature with the highest effect size
    df_results['Effect_Size_Value_Num'] = pd.to_numeric(df_results['Effect_Size_Value'], errors='coerce')
    strongest_predictor = df_results.loc[df_results['Effect_Size_Value_Num'].idxmax(), 'Research_Question']
    # Extract just the variable name from the question string (e.g. "Is GPA associated...")
    strongest_var = strongest_predictor.split(" ")[1].upper()
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Hypotheses Tested</div>
            <div class="metric-value">{total_tests}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Statistically Significant</div>
            <div class="metric-value">{significant_tests} / {total_tests}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Strongest Predictor</div>
            <div class="metric-value">{strongest_var}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ---------------------------------------------------------
    # TABS FOR CONTENT ORGANIZATION
    # ---------------------------------------------------------
    tab1, tab2 = st.tabs(["📊 Interactive Test Results", "🧠 Academic Methodology"])
    
    with tab1:
        st.markdown("### 🧪 Comprehensive Hypothesis Testing Summary")
        
        # Pandas Styler for a gorgeous dataframe
        def highlight_significant(val):
            color = '#d4edda' if val == 'Yes' else '#f8d7da'
            text_color = '#155724' if val == 'Yes' else '#721c24'
            return f'background-color: {color}; color: {text_color}; font-weight: bold'
            
        def highlight_magnitude(val):
            if val == 'Large': return 'background-color: #cce5ff; color: #004085; font-weight: bold'
            elif val == 'Medium': return 'background-color: #fff3cd; color: #856404'
            elif val == 'Small': return 'background-color: #e2e3e5; color: #383d41'
            return ''

        # Drop the temporary numeric column before displaying
        display_df = df_results.drop(columns=['Effect_Size_Value_Num'])
        
        styled_df = display_df.style.map(
            highlight_significant, subset=['Significant']
        ).map(
            highlight_magnitude, subset=['Effect_Magnitude']
        ).set_properties(**{
            'text-align': 'left',
            'border-color': 'white'
        })
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True, height=300)
        
        st.caption("👈 Use the scrollbar or click column headers to sort the results!")
        
    with tab2:
        st.markdown("### 🔍 Advanced Statistical Interpretation")
        st.markdown("""
        This dashboard goes beyond standard introductory statistics by employing rigorous, academic-grade methodologies. Here is how to interpret the advanced metrics above:
        """)
        
        st.info("**1. The False Discovery Rate (FDR) & Adjusted P-Values**")
        st.markdown("""
        When running multiple statistical tests simultaneously, the chance of getting a 'false positive' (Type I error) increases exponentially. To prevent this, our R backend applies the **Benjamini-Hochberg FDR correction**. 
        
        The **`Formatted_Adj_P_Value`** column is much stricter than a normal p-value. If this value is still `< 0.05`, we can be mathematically certain that the relationship is genuine.
        """)
        
        st.success("**2. Effect Size (Cohen's d & Cramer's V)**")
        st.markdown("""
        A p-value only tells us *if* a relationship exists, but it doesn't tell us if that relationship actually matters in the real world. That is what **Effect Size** is for!
        * **Cohen's d:** Used for our t-tests (like GPA). A score of 0.2 is Small, 0.5 is Medium, and 0.8+ is Large.
        * **Cramer's V:** Used for our Chi-Square tests (like categorical variables). A score of 0.05 is Small, 0.15 is Medium, and 0.25+ is Large.
        
        The **`Effect_Magnitude`** column automatically categorizes these mathematical scores into human-readable labels so you can easily spot the most powerful predictors of employment!
        """)
else:
    st.error("Statistical results file not found. Please run the R backend script first to generate `res/all_results.csv`.")
