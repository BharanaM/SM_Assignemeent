# 🚀 Project Update Report: Graduate Employment Analysis
**Date:** September 30, 2026  
**Focus:** Complete R-Backend Migration, Advanced Phase 3 Analytics, and Streamlit Dashboard Overhaul

---

## 1. 📂 Architecture & Directory Restructuring
To align strictly with the requirement that all analytical and predictive workloads be handled in R, the project structure was heavily sanitized and reorganized:
* **Data Hierarchy:** Reorganized the dataset storage into `data/raw/` and `data/preprocessed/` subdirectories to maintain a strict pipeline flow.
* **Obsolete Python Removal:** Deleted all legacy Python backend scripts from `src/` (e.g., `data_cleaning.py`, `models.py`, `inference.py`) and `scripts/10_run_all.py`. 
* **Model Cleanup:** Removed all Python `.joblib` model binaries, leaving only the authoritative R `.rds` models in the `models/` directory.
* **Artifact Cleanup:** Safely wiped the obsolete `res/` directory and old CSV/PNG files. All fresh tables and figures are now generated directly by R into `outputs/tables/` and `outputs/figures/`.

## 2. 📊 R Pipeline Enhancements (Backend)
The R pipeline was heavily upgraded to meet "Phase 3" advanced requirements:
* **Data Cleaning & EDA (`01_cleaning_and_eda.R`):** 
  * Implemented a comprehensive **Missing Value Analysis** and **IQR Outlier Detection**.
  * Added a numeric **Correlation Matrix** generator to detect feature multicollinearity.
* **Rigorous Statistical Inference (`02_statistical_inference.R`):** 
  * Expanded hypothesis testing beyond basic t-tests and Chi-Square.
  * Implemented **F-Tests / Levene's Test** for variance analysis.
  * Added **ANOVA** paired with **Tukey HSD** post-hoc tests for multi-group comparisons (e.g., GPA across Education Levels).
  * Added **2-Sample Proportions Tests** for categorical rate comparisons (e.g., Internship rates by Employment status).
* **Advanced Predictive Modeling (`03_modelling.R`):** 
  * Migrated all machine learning to R.
  * Trained **Logistic Regression** (with VIF multicollinearity checks and Odds Ratio extraction), **LASSO Regularization** (via cross-validated `glmnet`), and a **Random Forest** benchmark.
  * Extracted rigorous, multi-metric evaluations (Accuracy, Precision, Recall, F1-Score, AUC).
* **PCA & Bayesian Inference (`04_pca_and_bayesian.R`):** 
  * Implemented **Task 7**: Dimensionality Reduction via **Principal Component Analysis (PCA)** on continuous variables, generating a visual Scree Plot and variance loadings.
  * Implemented **Task 8**: Probabilistic classification using a **Naive Bayes** model, achieving ~92.2% Sensitivity (Recall).

## 3. 🎨 Streamlit Frontend Enhancements (UI)
The Python Streamlit application was overhauled to beautifully present the new R artifacts:
* **Exploratory Analysis (`02_Exploratory_Analysis.py`):** 
  * Added a new **"Data Quality & Diagnostics"** tab.
  * Dynamically loads the R-generated Missing Value Summary, Outlier logs, and renders the Correlation Matrix with a custom heatmap gradient.
* **Statistical Inference (`03_Statistical_Inference.py`):** 
  * Appended beautiful UI metric cards summarizing the results of the Phase 3 advanced inference tests (Levene's, ANOVA, Proportions).
* **New Page: PCA & Bayesian (`05_PCA_and_Bayesian.py`):** 
  * Created a brand-new dedicated page to highlight Tasks 7 and 8.
  * Displays the PCA Scree plot alongside business conclusions regarding dimensionality reduction.
  * Displays the detailed Naive Bayes Confusion Matrix and performance breakdown.
* **Model Performance Dashboard (`06_Model_Performance.py`):** 
  * Completely redesigned into a highly professional, multi-metric comparison dashboard.
  * Replaced the basic accuracy chart with an interactive **Plotly Radar Chart** and **Bar Chart** comparing all four models (Logistic, LASSO, RF, Naive Bayes) across Accuracy, Precision, Recall, F1-Score, and AUC.
* **Prediction Engine (`04_Employment_Prediction.py`):** 
  * Fixed a critical Windows pathing crash (Exit code `0xC0000005`) by updating the `subprocess` hook to correctly route live user inputs to the new `R/predict_new.R` script, allowing seamless frontend predictions powered by the R backend.

---
*End of Report*
