import streamlit as st

def categorical_chart(df, column: str):
    st.bar_chart(df[column].value_counts())
