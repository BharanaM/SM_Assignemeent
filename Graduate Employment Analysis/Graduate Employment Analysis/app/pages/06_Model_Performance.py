from pathlib import Path
import sys
import pandas as pd
import streamlit as st
import plotly.express as px
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.config import TABLE_DIR

st.set_page_config(page_title="Model Performance", page_icon="⚙️", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1 { color: #1E3A8A; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

st.title("⚙️ Machine Learning Model Performance")
st.markdown("Compare the evaluation metrics across all trained classification models.")

metrics_file = TABLE_DIR / "employment_model_metrics.csv"
if metrics_file.exists():
    df_metrics = pd.read_csv(metrics_file)
    
    st.subheader("📊 Accuracy Comparison")
    # Interactive Plotly Bar Chart comparing models
    fig = px.bar(df_metrics, x='model', y='accuracy', text='accuracy', 
                 color='model', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_traces(texttemplate='%{text:.2%}', textposition='outside')
    fig.update_layout(yaxis_title="Accuracy", xaxis_title="", showlegend=False, yaxis_range=[0, 1.1])
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📋 Detailed Metrics Table")
    
    # Format the dataframe nicely
    formatted_df = df_metrics.copy()
    for col in formatted_df.columns:
        if col != 'model':
            formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:.2%}")
            
    st.dataframe(formatted_df, use_container_width=True, hide_index=True)
    
else:
    st.error("No model metrics found. Please train the models first.")

st.info("💡 **Note:** Model selection should balance high accuracy with interpretability, calibration, and organizational usefulness.")
