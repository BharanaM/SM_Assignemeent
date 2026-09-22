from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "dataset.csv"
OUTPUT_PATH = BASE_DIR / "dataset_predictive.csv"

# Load the dataset
df = pd.read_csv(DATA_PATH)

# Set random seed for reproducibility
np.random.seed(42)
n = len(df)

# Create boolean masks for our target variables
emp_mask = df['Employment_Status'] == 'Employed'
cont_mask = df['Employment_Status'] == 'Continuing Education'
unemp_mask = df['Employment_Status'] == 'Unemployed'

# ==========================================
# 1. FIX GPA
# ==========================================
# Shift distributions: Employed (mean 3.5), Continuing Ed (mean 3.7), Unemployed (mean 2.6)
df['GPA'] = np.select(
    [emp_mask, cont_mask],
    [np.random.normal(3.5, 0.3, size=n), np.random.normal(3.7, 0.2, size=n)],
    default=np.random.normal(2.6, 0.4, size=n)
)
df['GPA'] = np.clip(df['GPA'], 1.0, 4.0).round(2)

# ==========================================
# 2. FIX UNIVERSITY RANKING
# ==========================================
# High ranking dominates Employed/High Salary; Low ranking dominates Unemployed
emp_high_sal_rank = emp_mask | (df['Salary'] > 60000)
cont_only = cont_mask & ~emp_high_sal_rank

df.loc[emp_high_sal_rank, 'University_Ranking'] = np.random.choice(
    ['High', 'Medium', 'Low'], p=[0.70, 0.20, 0.10], size=emp_high_sal_rank.sum()
)
df.loc[cont_only, 'University_Ranking'] = np.random.choice(
    ['High', 'Medium', 'Low'], p=[0.40, 0.40, 0.20], size=cont_only.sum()
)
df.loc[~(emp_high_sal_rank | cont_only), 'University_Ranking'] = np.random.choice(
    ['High', 'Medium', 'Low'], p=[0.10, 0.30, 0.60], size=(~(emp_high_sal_rank | cont_only)).sum()
)

# ==========================================
# 3. FIX FIELD OF STUDY
# ==========================================
# STEM fields get higher probability of mapping to Employed
stem_fields = ['IT', 'Engineering', 'Health']
non_stem = ['Arts', 'Business', 'Social Sciences']

df.loc[emp_mask, 'Field_of_Study'] = np.random.choice(
    stem_fields + non_stem, p=[0.25, 0.25, 0.20, 0.10, 0.10, 0.10], size=emp_mask.sum()
)
df.loc[~emp_mask, 'Field_of_Study'] = np.random.choice(
    stem_fields + non_stem, p=[0.10, 0.10, 0.10, 0.25, 0.25, 0.20], size=(~emp_mask).sum()
)

# ==========================================
# 4. FIX REGION OF STUDY & COUNTRY OF ORIGIN
# ==========================================
# Establish EU and Canada as regions with higher employment placement rates
regions = ['EU', 'UK', 'Canada', 'Australia']
df.loc[emp_mask, 'Region_of_Study'] = np.random.choice(
    regions, p=[0.40, 0.10, 0.35, 0.15], size=emp_mask.sum()
)
df.loc[~emp_mask, 'Region_of_Study'] = np.random.choice(
    regions, p=[0.15, 0.35, 0.15, 0.35], size=(~emp_mask).sum()
)

# Assign a slight bias for certain countries based on employment
countries = df['Country_of_Origin'].unique().tolist()
df.loc[emp_mask, 'Country_of_Origin'] = np.random.choice(
    countries, p=[0.2, 0.2, 0.15, 0.15, 0.1, 0.1, 0.05, 0.05], size=emp_mask.sum() 
)
df.loc[~emp_mask, 'Country_of_Origin'] = np.random.choice(
    countries, p=[0.05, 0.05, 0.1, 0.1, 0.15, 0.15, 0.2, 0.2], size=(~emp_mask).sum() 
)

# ==========================================
# 5. FIX EDUCATION LEVEL (Stratified by Salary)
# ==========================================
# Break the employed mask into salary tiers to create a realistic correlation
emp_high_sal = emp_mask & (df['Salary'] >= 65000)
emp_med_sal = emp_mask & (df['Salary'] >= 45000) & (df['Salary'] < 65000)
emp_low_sal = emp_mask & (df['Salary'] < 45000)

# Assign degrees based on salary tiers
df.loc[emp_high_sal, 'Education_Level'] = np.random.choice(
    ['PhD', "Master's", "Bachelor's", 'Diploma'], 
    p=[0.60, 0.35, 0.05, 0.00], 
    size=emp_high_sal.sum()
)

df.loc[emp_med_sal, 'Education_Level'] = np.random.choice(
    ['PhD', "Master's", "Bachelor's", 'Diploma'], 
    p=[0.10, 0.50, 0.35, 0.05], 
    size=emp_med_sal.sum()
)

df.loc[emp_low_sal, 'Education_Level'] = np.random.choice(
    ['PhD', "Master's", "Bachelor's", 'Diploma'], 
    p=[0.02, 0.18, 0.50, 0.30], 
    size=emp_low_sal.sum()
)

# Assign degrees to unemployed and continuing education
df.loc[cont_mask, 'Education_Level'] = np.random.choice(
    ['PhD', "Master's", "Bachelor's", 'Diploma'], 
    p=[0.05, 0.20, 0.60, 0.15], 
    size=cont_mask.sum()
)

df.loc[unemp_mask, 'Education_Level'] = np.random.choice(
    ['PhD', "Master's", "Bachelor's", 'Diploma'], 
    p=[0.02, 0.08, 0.40, 0.50], 
    size=unemp_mask.sum()
)

# ==========================================
# 6. FIX LANGUAGE PROFICIENCY
# ==========================================
# We want a clear hierarchy: Fluent > Advanced > Intermediate > Basic
df.loc[emp_mask, 'Language_Proficiency'] = np.random.choice(
    ['Fluent', 'Advanced', 'Intermediate', 'Basic'], 
    p=[0.45, 0.35, 0.15, 0.05], 
    size=emp_mask.sum()
)

df.loc[cont_mask, 'Language_Proficiency'] = np.random.choice(
    ['Fluent', 'Advanced', 'Intermediate', 'Basic'], 
    p=[0.20, 0.30, 0.35, 0.15], 
    size=cont_mask.sum()
)

df.loc[unemp_mask, 'Language_Proficiency'] = np.random.choice(
    ['Fluent', 'Advanced', 'Intermediate', 'Basic'], 
    p=[0.05, 0.15, 0.40, 0.40], 
    size=unemp_mask.sum()
)

# ==========================================
# 7. SAVE OUTPUT
# ==========================================
df.to_csv(OUTPUT_PATH, index=False)
print(f"Transformation complete. Predictive features successfully injected. Output saved to: {OUTPUT_PATH}")