args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  stop("No JSON input provided.")
}

suppressPackageStartupMessages({
  library(jsonlite)
  library(randomForest)
  library(caret)
  library(dplyr)
})

# Dynamically set working directory to project root (works on Windows, Linux, Streamlit Cloud)
script_args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("--file=", script_args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- sub("--file=", "", file_arg[1])
  project_root <- normalizePath(file.path(dirname(script_path), ".."), winslash = "/")
  if (dir.exists(project_root)) {
    setwd(project_root)
  }
}

# Read input JSON
input_data <- fromJSON(args[1])

# Load the trained R models (using absolute paths)
model_path <- "models/employment_model_R.rds"
salary_model_path <- "models/salary_model_R.rds"

if (!file.exists(model_path)) {
  stop("Employment model file not found. Please run train_model.R first.")
}

rf_model <- readRDS(model_path)
lm_salary <- if (file.exists(salary_model_path)) readRDS(salary_model_path) else NULL

# Ensure factor levels match by loading a skeleton of the training data
data_path <- "data/preprocessed/dataset_predictive.csv"
if(file.exists(data_path)) {
    data <- read.csv(data_path, stringsAsFactors = TRUE)
    
    # Force the input data to have exactly the same factor levels as the training data
    for (col in names(input_data)) {
        if (col %in% names(data) && is.factor(data[[col]])) {
            input_data[[col]] <- factor(input_data[[col]], levels = levels(data[[col]]))
        }
    }
    combined <- input_data
} else {
    combined <- input_data
}

# Predict
prob_preds <- predict(rf_model, combined, type="prob")
emp_prob <- as.numeric(prob_preds[1, "Employed"])

predicted_salary <- if (!is.null(lm_salary)) as.numeric(predict(lm_salary, combined)[1]) else NULL

# Output JSON result so Python can read it
result <- list(
  employed_probability = emp_prob,
  predicted_salary = predicted_salary
)
cat(toJSON(result, auto_unbox = TRUE))
