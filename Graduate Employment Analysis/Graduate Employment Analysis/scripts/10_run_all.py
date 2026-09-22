from pathlib import Path
import sys
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import RAW_DATA, PROCESSED_DATA, OUTPUT_DIR, TABLE_DIR, FIGURE_DIR, MODEL_DIR
from src.data_loader import load_raw
from src.data_cleaning import clean_data, save_quality_report
from src.eda import write_eda_outputs
from src.inference import run_inference
from src.models import train_models

def main():
    for path in [PROCESSED_DATA.parent, TABLE_DIR, FIGURE_DIR, MODEL_DIR]:
        path.mkdir(parents=True, exist_ok=True)
    print("Loading and validating raw data...", flush=True)
    df, quality = clean_data(load_raw(RAW_DATA))
    print(f"Cleaned dataset: {len(df):,} rows.", flush=True)
    df.to_csv(PROCESSED_DATA, index=False)
    save_quality_report(quality, TABLE_DIR / "data_quality_report.csv")
    pd.DataFrame([{"metric": k, "value": v} for k, v in quality.items() if k not in {"dtypes", "categorical_levels", "ranges", "suspicious_values"}]).to_csv(TABLE_DIR / "dataset_summary.csv", index=False)
    print("Generating descriptive tables and figures...", flush=True)
    write_eda_outputs(df, TABLE_DIR, FIGURE_DIR)
    print("Running statistical inference...", flush=True)
    run_inference(df, TABLE_DIR / "statistical_results.csv")
    print("Training employment models...", flush=True)
    train_models(df, MODEL_DIR, TABLE_DIR)
    print(f"Completed analysis for {len(df):,} cleaned observations.")

if __name__ == "__main__":
    main()
