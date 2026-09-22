from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from .config import CATEGORICAL_COLUMNS, NUMERICAL_COLUMNS

def write_eda_outputs(df: pd.DataFrame, table_dir: Path, figure_dir: Path) -> None:
    table_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)
    for col in CATEGORICAL_COLUMNS:
        df[col].value_counts(dropna=False).rename_axis(col).reset_index(name="count").assign(
            percentage=lambda x: x["count"] / len(df) * 100
        ).to_csv(table_dir / f"{col}_frequency.csv", index=False)
    df[NUMERICAL_COLUMNS].describe().T.to_csv(table_dir / "numerical_summary.csv")
    df[NUMERICAL_COLUMNS].corr().to_csv(table_dir / "correlation_matrix.csv")
    for col in CATEGORICAL_COLUMNS[:9] + ["employment_status", "job_sector"]:
        plt.figure(figsize=(9, 5))
        order = df[col].value_counts().index
        sns.countplot(data=df, y=col, order=order)
        plt.title(f"Distribution of {col.replace('_', ' ').title()}")
        plt.tight_layout()
        plt.savefig(figure_dir / f"{col}.png", dpi=160)
        plt.close()
    for col in NUMERICAL_COLUMNS:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col], bins=30, kde=True)
        plt.title(f"Distribution of {col.replace('_', ' ').title()}")
        plt.tight_layout()
        plt.savefig(figure_dir / f"{col}_distribution.png", dpi=160)
        plt.close()
    for col in ["education_level", "field_of_study", "language_proficiency", "internship_experience", "university_ranking"]:
        table = pd.crosstab(df[col], df["employment_status"], normalize="index") * 100
        table.to_csv(table_dir / f"employment_by_{col}.csv")
        table.plot(kind="bar", stacked=True, figsize=(10, 5))
        plt.ylabel("Percentage")
        plt.title(f"Employment status by {col.replace('_', ' ').title()}")
        plt.tight_layout()
        plt.savefig(figure_dir / f"employment_by_{col}.png", dpi=160)
        plt.close()
    plt.figure(figsize=(8, 6))
    sns.heatmap(df[NUMERICAL_COLUMNS].corr(), annot=True, cmap="vlag", center=0)
    plt.tight_layout()
    plt.savefig(figure_dir / "correlation_heatmap.png", dpi=160)
    plt.close()
