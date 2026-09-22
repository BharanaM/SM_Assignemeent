from pathlib import Path
import pandas as pd
from .config import CATEGORICAL_COLUMNS, NUMERICAL_COLUMNS

def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    original_rows = len(df)
    duplicate_rows = int(df.duplicated().sum())
    out = df.copy()
    for col in CATEGORICAL_COLUMNS:
        out[col] = out[col].astype("string").str.strip()
    missing_before = int(out.isna().sum().sum())
    suspicious = {
        "age_out_of_range": int((~out["age"].between(16, 100)).sum()),
        "years_since_graduation_negative": int((out["years_since_graduation"] < 0).sum()),
        "gpa_out_of_range": int((~out["gpa"].between(0, 4.0)).sum()),
        "salary_negative": int((out["salary"] < 0).sum()),
    }
    out = out.drop_duplicates().reset_index(drop=True)
    quality = {
        "original_rows": original_rows,
        "duplicate_rows": duplicate_rows,
        "final_rows": len(out),
        "columns": len(out.columns),
        "missing_values": int(out.isna().sum().sum()),
        "missing_by_column": out.isna().sum().to_dict(),
        "missing_value_note": (
            "Job sector is missing for non-employed graduates, consistent with a "
            "post-employment outcome variable; values were retained and not imputed."
            if out["job_sector"].isna().any() else ""
        ),
        "suspicious_values": suspicious,
        "dtypes": out.dtypes.astype(str).to_dict(),
        "categorical_levels": {c: int(out[c].nunique()) for c in CATEGORICAL_COLUMNS},
        "ranges": {c: {"min": float(out[c].min()), "max": float(out[c].max())} for c in NUMERICAL_COLUMNS},
    }
    return out, quality

def save_quality_report(quality: dict, path: Path) -> None:
    rows = []
    for key, value in quality.items():
        rows.append({"metric": key, "value": str(value)})
    pd.DataFrame(rows).to_csv(path, index=False)
