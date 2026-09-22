# Graduate Employment Analysis

Reproducible Python analysis of graduate employment and salary associations.

## Run

From this directory:

```powershell
python scripts\10_run_all.py
streamlit run app\streamlit_app.py
```

The raw data must be at `data/dataset.csv`. The pipeline removes exact duplicate
rows only, reports suspicious values, preserves the observed categories, and
does not claim causal effects. Employment prediction defines the binary target
explicitly as `Employed` versus all other observed employment-status classes.
Salary modelling is restricted to employed graduates and does not use `salary`
or `job_sector` as predictors.

The dataset has no comprehensive soft-skills battery, so communication,
teamwork, leadership, and similar skills cannot be estimated directly.
