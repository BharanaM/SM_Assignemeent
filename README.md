# Graduate Employment Analysis

Statistical modeling project for exploring graduate employment outcomes and predicting employment status and salary.

## Project structure

- `Graduate Employment Analysis/` - Streamlit application, analysis scripts, data, and model code
- `train_and_predict.py` - top-level prediction script

## Setup

Create and activate a virtual environment, then install the project requirements:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r "Graduate Employment Analysis\Graduate Employment Analysis\requirements.txt"
```

Run the Streamlit application from the application directory:

```powershell
cd "Graduate Employment Analysis\Graduate Employment Analysis"
streamlit run app\streamlit_app.py
```

Generated model binaries and local environment files are intentionally excluded from Git because of their size.