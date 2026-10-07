from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "outputs" / "tables"

@st.cache_data
def read_table(name: str) -> pd.DataFrame:
    return pd.read_csv(TABLE_DIR / name)

def note(text: str) -> None:
    st.info(text)
