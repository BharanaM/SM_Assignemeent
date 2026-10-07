args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  stop("No JSON input provided.")
}

library(here)
library(jsonlite)
library(randomForest)
library(dplyr)

# Read input JSON
input_data <- fromJSON(args[1])

# Load the trained R model (using absolute paths)
model_path <- here("models", "employment_model_R.rds")
if (!file.exists(model_path)) {
  stop("Model file not found. Please run train_model.R first.")
}
rf_model <- readRDS(model_path)

# Ensure factor levels match by loading a skeleton of the training data
data_path <- here("data", "preprocessed", "dataset_predictive.csv")
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
emp_prob <- prob_preds[1, "Employed"]

# Output JSON result so Python can read it
result <- list(employed_probability = emp_prob)
cat(toJSON(result, auto_unbox = TRUE))
