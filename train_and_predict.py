import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import classification_report, mean_squared_error, r2_score
import joblib

# File path to the dataset
FILE_PATH = r"C:\Users\user\OneDrive - Sri Lanka Institute of Information Technology\OOP\Documents\SLIIT 3.1\IT3081 - Statistical Modeling\Graduate Employment Analysis\Graduate Employment Analysis\Graduate Employment Analysis\dataset_predictive.csv"

def load_and_preprocess_data(file_path):
    print("Loading dataset...")
    df = pd.read_csv(file_path)
    
    # Target columns
    target_class = 'Employment_Status'
    target_reg = 'Salary'
    
    # Define feature columns (excluding 'Job_Sector' because it's an outcome)
    categorical_cols = ['Country_of_Origin', 'Education_Level', 'Field_of_Study', 
                        'Language_Proficiency', 'Visa_Type', 'Gender', 
                        'University_Ranking', 'Region_of_Study', 'Internship_Experience']
    numerical_cols = ['Age', 'Years_Since_Graduation', 'GPA']
    
    features = categorical_cols + numerical_cols
    
    # 1. Binary classification: 1 if Employed, 0 otherwise
    df['Is_Employed'] = (df[target_class] == 'Employed').astype(int)
    
    return df, features, categorical_cols, numerical_cols

def build_pipelines(categorical_cols, numerical_cols):
    # Preprocessing for numerical data
    numerical_transformer = StandardScaler()
    
    # Preprocessing for categorical data
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    
    # Bundle preprocessing for numerical and categorical data
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])
    
    # Define models
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    reg = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Bundle preprocessing and modeling code in a pipeline
    clf_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                   ('model', clf)])
                                   
    reg_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                   ('model', reg)])
                                   
    return clf_pipeline, reg_pipeline

def train_models():
    df, features, cat_cols, num_cols = load_and_preprocess_data(FILE_PATH)
    
    X = df[features]
    y_clf = df['Is_Employed']
    
    print("\n--- Training Classification Model (Employment Status) ---")
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_clf, test_size=0.2, random_state=42)
    
    clf_pipeline, reg_pipeline = build_pipelines(cat_cols, num_cols)
    clf_pipeline.fit(X_train_c, y_train_c)
    
    # Evaluate Classifier
    y_pred_c = clf_pipeline.predict(X_test_c)
    print("Classification Report:")
    print(classification_report(y_test_c, y_pred_c))
    
    print("\n--- Training Regression Model (Salary) ---")
    # For salary prediction, we only train on people who are actually employed (Salary > 0)
    employed_df = df[df['Is_Employed'] == 1]
    X_reg = employed_df[features]
    y_reg = employed_df['Salary']
    
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
    reg_pipeline.fit(X_train_r, y_train_r)
    
    # Evaluate Regressor
    y_pred_r = reg_pipeline.predict(X_test_r)
    mse = mean_squared_error(y_test_r, y_pred_r)
    r2 = r2_score(y_test_r, y_pred_r)
    rmse = np.sqrt(mse)
    print(f"Regression RMSE: ${rmse:,.2f}")
    print(f"Regression R2 Score: {r2:.2f}")
    
    # Save the models
    joblib.dump(clf_pipeline, 'employment_classifier.pkl')
    joblib.dump(reg_pipeline, 'salary_regressor.pkl')
    print("\n[+] Models saved successfully to 'employment_classifier.pkl' and 'salary_regressor.pkl'.")

def predict_new_applicant(features_dict):
    """
    Predicts the likelihood of employment and expected salary for a new applicant.
    """
    try:
        clf_pipeline = joblib.load('employment_classifier.pkl')
        reg_pipeline = joblib.load('salary_regressor.pkl')
    except FileNotFoundError:
        print("Model files not found. Please train the models first.")
        return
        
    df_new = pd.DataFrame([features_dict])
    
    employment_pred = clf_pipeline.predict(df_new)[0]
    employment_prob = clf_pipeline.predict_proba(df_new)[0][1]
    
    salary_pred = reg_pipeline.predict(df_new)[0]
    
    status = "Employed" if employment_pred == 1 else "Not Employed"
    print(f"\n--- Prediction Results for Sample Applicant ---")
    print(f"Predicted Status: {status} (Probability of being employed: {employment_prob:.2%})")
    if employment_pred == 1:
        print(f"Expected Salary: ${salary_pred:,.2f}")
    else:
        print(f"Expected Salary if Employed: ${salary_pred:,.2f} (Though predicted as not employed)")
        
if __name__ == "__main__":
    # Train the models and save them
    train_models()
    
    # Test Prediction with a sample requirement
    sample_student = {
        'Country_of_Origin': 'India',
        'Education_Level': "Master's",
        'Field_of_Study': 'IT',
        'Language_Proficiency': 'Fluent',
        'Visa_Type': 'Post-study',
        'Gender': 'Female',
        'University_Ranking': 'High',
        'Region_of_Study': 'UK',
        'Internship_Experience': 'Yes',
        'Age': 26,
        'Years_Since_Graduation': 2,
        'GPA': 3.8
    }
    
    predict_new_applicant(sample_student)
