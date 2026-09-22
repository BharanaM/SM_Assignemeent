from pathlib import Path
import pandas as pd

EXPECTED_COLUMNS = {
    "country_of_origin", "education_level", "field_of_study",
    "language_proficiency", "visa_type", "gender", "university_ranking",
    "region_of_study", "age", "years_since_graduation", "gpa",
    "internship_experience", "employment_status", "salary", "job_sector",
}

def load_raw(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    missing = EXPECTED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    return df
