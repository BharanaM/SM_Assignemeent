from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
                             average_precision_score, mean_absolute_error, mean_squared_error, r2_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from .config import PRE_EMPLOYMENT_COLUMNS, RANDOM_STATE

def _preprocessor(X):
    cats = X.select_dtypes(exclude="number").columns.tolist()
    nums = X.select_dtypes(include="number").columns.tolist()
    return ColumnTransformer([("categorical", OneHotEncoder(handle_unknown="ignore"), cats),
                              ("numeric", StandardScaler(), nums)])

def train_models(df: pd.DataFrame, model_dir: Path, table_dir: Path) -> dict:
    model_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)
    X = df[PRE_EMPLOYMENT_COLUMNS]
    y = (df["employment_status"] == "Employed").astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, stratify=y, random_state=RANDOM_STATE)
    employment_metrics = []
    for name, estimator in [
        ("Logistic Regression", LogisticRegression(max_iter=1000)),
        ("Ridge Logistic Regression", LogisticRegression(penalty="l2", C=1.0, max_iter=1000)),
        ("LASSO Logistic Regression", LogisticRegression(penalty="l1", solver="liblinear", max_iter=1000)),
        ("Random Forest", RandomForestClassifier(n_estimators=150, random_state=RANDOM_STATE, n_jobs=-1, max_depth=12)),
    ]:
        pipe = Pipeline([("preprocessor", _preprocessor(X_train)), ("model", estimator)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        prob = pipe.predict_proba(X_test)[:, 1]
        employment_metrics.append({"model": name, "accuracy": accuracy_score(y_test, pred),
            "precision": precision_score(y_test, pred, zero_division=0), "recall": recall_score(y_test, pred, zero_division=0),
            "specificity": recall_score(1-y_test, 1-pred, zero_division=0), "f1": f1_score(y_test, pred, zero_division=0),
            "roc_auc": roc_auc_score(y_test, prob), "pr_auc": average_precision_score(y_test, prob)})
        if name == "Logistic Regression":
            joblib.dump(pipe, model_dir / "employment_model.joblib")
    pd.DataFrame(employment_metrics).to_csv(table_dir / "employment_model_metrics.csv", index=False)
    joblib.dump({"employment_features": PRE_EMPLOYMENT_COLUMNS,
                 "target_definition": "Employed versus all other observed employment-status classes."}, model_dir / "metadata.joblib")
    joblib.dump({"employment_preprocessor": employment_metrics},
                model_dir / "preprocessors.joblib")
    return {"employment": employment_metrics}
