from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

def run_inference(df: pd.DataFrame, path: Path) -> pd.DataFrame:
    rows = []
    employed = df.loc[df.employment_status == "Employed", "gpa"]
    not_employed = df.loc[df.employment_status != "Employed", "gpa"]
    t = stats.ttest_ind(employed, not_employed, equal_var=False)
    diff = employed.mean() - not_employed.mean()
    se = np.sqrt(employed.var(ddof=1) / len(employed) + not_employed.var(ddof=1) / len(not_employed))
    ci = stats.t.interval(0.95, len(employed) + len(not_employed) - 2, loc=diff, scale=se)
    rows.append({"research_question": "Is GPA associated with employment status?",
                 "null_hypothesis": "Mean GPA is equal for employed and not-employed graduates.",
                 "alternative_hypothesis": "Mean GPA differs between groups.", "test": "Welch t-test",
                 "statistic": t.statistic, "p_value": t.pvalue, "effect_size": diff,
                 "confidence_interval": f"[{ci[0]:.4f}, {ci[1]:.4f}]",
                 "interpretation": "Association only; observational data cannot establish causality."})
    categorical = ["education_level", "field_of_study", "language_proficiency",
                   "internship_experience", "university_ranking"]
    p_values = []
    for col in categorical:
        table = pd.crosstab(df[col], df.employment_status)
        result = stats.chi2_contingency(table)
        n = table.to_numpy().sum()
        effect = np.sqrt(result[0] / (n * min(table.shape[0] - 1, table.shape[1] - 1)))
        rows.append({"research_question": f"Is {col} associated with employment status?",
                     "null_hypothesis": f"{col} and employment status are independent.",
                     "alternative_hypothesis": f"{col} and employment status are associated.",
                     "test": "Chi-square test of independence", "statistic": result[0],
                     "p_value": result[1], "effect_size": effect,
                     "confidence_interval": "", "interpretation": "Association, not causation."})
        p_values.append(result[1])
    adjusted = multipletests(p_values, method="fdr_bh")[1]
    for row, adj in zip(rows[-len(categorical):], adjusted):
        row["adjusted_p_value"] = adj
    result_df = pd.DataFrame(rows)
    result_df.to_csv(path, index=False)
    return result_df
