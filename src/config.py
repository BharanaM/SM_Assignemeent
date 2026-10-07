from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DATA = DATA_DIR / "raw" / "dataset_predictive.csv"
PROCESSED_DATA = DATA_DIR / "preprocessed" / "dataset_predictive.csv"
OUTPUT_DIR = ROOT / "Outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"
TABLE_DIR = OUTPUT_DIR / "tables"
MODEL_DIR = ROOT / "models"

CATEGORICAL_COLUMNS = [
    "country_of_origin", "education_level", "field_of_study",
    "language_proficiency", "visa_type", "gender", "university_ranking",
    "region_of_study", "internship_experience", "employment_status",
    "job_sector",
]
NUMERICAL_COLUMNS = ["age", "years_since_graduation", "gpa", "salary"]
PRE_EMPLOYMENT_COLUMNS = [
    "country_of_origin", "education_level", "field_of_study",
    "language_proficiency", "visa_type", "gender", "university_ranking",
    "region_of_study", "age", "years_since_graduation", "gpa",
    "internship_experience",
]
RANDOM_STATE = 42
