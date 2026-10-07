# Install required packages if not already installed
packages <- c("randomForest", "caret", "dplyr")
new_packages <- packages[!(packages %in% installed.packages()[,"Package"])]
if(length(new_packages)) install.packages(new_packages, repos = "http://cran.us.r-project.org")

library(here)
library(randomForest)
library(caret)
library(dplyr)

# Setup file paths
file_path <- here("data", "preprocessed", "dataset_predictive.csv")

cat("Loading data...\n")
if (!file.exists(file_path)) {
  stop("Dataset not found at the specified path.")
}

# Read CSV and convert strings to factors for Random Forest
data <- read.csv(file_path, stringsAsFactors = TRUE)

cat("Preparing data for Employment Prediction...\n")
# We remove Salary and Job Sector as they are outcomes of being employed
data <- data %>% select(-salary, -job_sector)

# Convert Target Variable to Binary classification (Employed vs Not Employed)
data$Is_Employed <- as.factor(ifelse(data$employment_status == "Employed", "Employed", "Not_Employed"))
data <- data %>% select(-employment_status)

# Split data into training and test sets (80% train, 20% test)
set.seed(42)
trainIndex <- createDataPartition(data$Is_Employed, p = .8, list = FALSE, times = 1)
dataTrain <- data[ trainIndex,]
dataTest  <- data[-trainIndex,]

cat("Training Random Forest classification model...\n")
# Limiting ntree to 50 for performance on large datasets. Increase this for more accuracy.
rf_model <- randomForest(Is_Employed ~ ., data = dataTrain, ntree = 50, importance = TRUE)

cat("\n--- Model Evaluation ---\n")
predictions <- predict(rf_model, dataTest)
prob_preds <- predict(rf_model, dataTest, type="prob")[, "Employed"]

conf_matrix <- confusionMatrix(predictions, dataTest$Is_Employed, positive="Employed")
print(conf_matrix)

# Print Feature Importance
cat("\n--- Feature Importance ---\n")
print(importance(rf_model))

# Calculate metrics for Streamlit CSV
accuracy <- conf_matrix$overall['Accuracy']
precision <- conf_matrix$byClass['Pos Pred Value']
recall <- conf_matrix$byClass['Sensitivity']
specificity <- conf_matrix$byClass['Specificity']
f1 <- conf_matrix$byClass['F1']
roc_auc <- NA # Skip for simplicity or use pROC
pr_auc <- NA

# Append to Streamlit's CSV
metrics_file <- here("outputs", "tables", "employment_model_metrics.csv")
if(file.exists(metrics_file)) {
  # Read existing
  existing_metrics <- read.csv(metrics_file)
  # Remove previous R model if exists
  existing_metrics <- existing_metrics %>% filter(model != "Random Forest (R)")
  # Create new row
  new_row <- data.frame(
    model = "Random Forest (R)",
    accuracy = as.numeric(accuracy),
    precision = as.numeric(precision),
    recall = as.numeric(recall),
    specificity = as.numeric(specificity),
    f1 = as.numeric(f1),
    roc_auc = as.numeric(roc_auc),
    pr_auc = as.numeric(pr_auc)
  )
  # Bind and save
  updated_metrics <- bind_rows(existing_metrics, new_row)
  write.csv(updated_metrics, metrics_file, row.names = FALSE)
  cat("\n[+] Added R Model metrics to Streamlit dashboard!\n")
}

# Save the model (using absolute path to avoid working directory errors)
model_save_path <- here("models", "employment_model_R.rds")
saveRDS(rf_model, model_save_path)
cat(sprintf("\n[+] Model successfully saved to: %s\n", model_save_path))

# Test Prediction with a sample requirement
cat("\n--- Testing Prediction on a New Applicant ---\n")
sample_student <- data.frame(
  country_of_origin = "India",
  education_level = "Master's",
  field_of_study = "IT",
  language_proficiency = "Fluent",
  visa_type = "Post-study",
  gender = "Female",
  university_ranking = "High",
  region_of_study = "UK",
  internship_experience = "Yes",
  age = 26,
  years_since_graduation = 2,
  gpa = 3.8
)

# Ensure factor levels match the training data
for (col in names(sample_student)) {
  if (is.factor(dataTrain[[col]])) {
    sample_student[[col]] <- factor(sample_student[[col]], levels = levels(dataTrain[[col]]))
  }
}

# Make prediction
employment_pred <- predict(rf_model, sample_student)
employment_prob <- predict(rf_model, sample_student, type = "prob")[1, "Employed"]

cat(sprintf("Predicted Status: %s (Probability of being employed: %.2f%%)\n", 
            as.character(employment_pred), employment_prob * 100))
