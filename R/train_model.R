# Install required packages if not already installed
packages <- c("randomForest", "caret", "dplyr", "gbm", "e1071", "glmnet")
new_packages <- packages[!(packages %in% installed.packages()[,"Package"])]
if(length(new_packages)) install.packages(new_packages, repos = "http://cran.us.r-project.org")

library(randomForest)
library(caret)
library(dplyr)
library(gbm)
library(e1071)
library(glmnet)

# Explicitly set working directory to avoid any path issues
try({
  args_full <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("--file=", args_full, value = TRUE)
  if (length(file_arg) > 0) {
    script_path <- sub("--file=", "", file_arg[1])
    setwd(normalizePath(file.path(dirname(script_path), ".."), winslash = "/"))
  } else if (!file.exists("data/preprocessed/dataset_predictive.csv")) {
    setwd("C:/Users/user/OneDrive - Sri Lanka Institute of Information Technology/OOP/Documents/SLIIT 3.1/IT3081 - Statistical Modeling/Graduate Employment Analysis")
  }
}, silent = TRUE)

# Setup file paths
file_path <- "data/preprocessed/dataset_predictive.csv"

cat("Loading data...\n")
if (!file.exists(file_path)) {
  stop("Dataset not found at the specified path.")
}

# Read CSV and convert strings to factors
data <- read.csv(file_path, stringsAsFactors = TRUE)

# ==============================================================================
# 1. EMPLOYMENT PREDICTION (CLASSIFICATION TOURNAMENT)
# ==============================================================================
cat("\n========================================================\n")
cat("Preparing data for Employment Prediction (Classification)\n")
cat("========================================================\n")

data_class <- data %>% select(-salary, -job_sector)
data_class$Is_Employed <- as.factor(ifelse(data_class$employment_status == "Employed", "Employed", "Not_Employed"))
data_class <- data_class %>% select(-employment_status)

set.seed(42)
trainIndex <- createDataPartition(data_class$Is_Employed, p = .8, list = FALSE, times = 1)
dataTrain <- data_class[trainIndex,]
dataTest  <- data_class[-trainIndex,]

# Set up Caret control to train exactly once (no CV loops) to save memory on 240k rows
train_control <- trainControl(method = "none", classProbs = TRUE)

cat("\n[1/3] Training Random Forest (optimized for low memory)...\n")
# Use explicit tuneGrid for method='none', and limit ntree to 50 like your original script
rf_grid <- data.frame(mtry = floor(sqrt(ncol(dataTrain))))
model_rf <- train(Is_Employed ~ ., data = dataTrain, method = "rf", 
                  trControl = train_control, tuneGrid = rf_grid, ntree = 50)

cat("[2/3] Training Gradient Boosting Machine (GBM)...\n")
gbm_grid <- expand.grid(n.trees = 50, interaction.depth = 3, shrinkage = 0.1, n.minobsinnode = 10)
model_gbm <- train(Is_Employed ~ ., data = dataTrain, method = "gbm", 
                   trControl = train_control, tuneGrid = gbm_grid, verbose = FALSE)

cat("[3/3] Training Penalized Logistic Regression (LASSO/Ridge/Elastic Net)...\n")
glmnet_grid <- expand.grid(alpha = 0.5, lambda = 0.01)
model_glmnet <- train(Is_Employed ~ ., data = dataTrain, method = "glmnet", 
                      trControl = train_control, tuneGrid = glmnet_grid)

# Compare Classification Models on the TEST set directly (saves memory)
cat("\nEvaluating models on 20% Test Set...\n")
eval_model <- function(model, name) {
  preds <- predict(model, dataTest)
  acc <- confusionMatrix(preds, dataTest$Is_Employed)$overall["Accuracy"]
  return(data.frame(Model = name, Accuracy = acc))
}

results_class <- rbind(
  eval_model(model_rf, "RandomForest"),
  eval_model(model_gbm, "GBM"),
  eval_model(model_glmnet, "GLMNET")
)
print(results_class)

# Find the best model based on Accuracy
best_model_name <- results_class$Model[which.max(results_class$Accuracy)]
cat(sprintf("\n🏆 BEST CLASSIFICATION MODEL: %s\n", best_model_name))

# Save Random Forest Model for Employment Prediction (as required for classification)
model_save_path <- "models/employment_model_R.rds"
if (!dir.exists("models")) dir.create("models", recursive = TRUE)
model_rf$trainingData <- NULL
saveRDS(model_rf, model_save_path, compress = "gzip")
cat(sprintf("[+] Random Forest Employment Model successfully saved to: %s\n", model_save_path))


# ==============================================================================
# 2. SALARY PREDICTION (REGRESSION TOURNAMENT)
# ==============================================================================
cat("\n========================================================\n")
cat("Preparing data for Salary Prediction (Regression)\n")
cat("========================================================\n")

data_reg <- data %>% filter(employment_status == "Employed")
data_reg <- data_reg %>% select(-job_sector, -employment_status)

set.seed(42)
trainIndex_reg <- createDataPartition(data_reg$salary, p = .8, list = FALSE)
regTrain <- data_reg[trainIndex_reg,]
regTest  <- data_reg[-trainIndex_reg,]

reg_control <- trainControl(method = "none")

cat("\n[1/3] Training Multiple Linear Regression...\n")
lm_grid <- expand.grid(intercept = TRUE)
model_lm <- train(salary ~ ., data = regTrain, method = "lm", trControl = reg_control, tuneGrid = lm_grid)

cat("[2/3] Training Gradient Boosting Machine (GBM) Regression...\n")
model_reg_gbm <- train(salary ~ ., data = regTrain, method = "gbm", 
                       trControl = reg_control, tuneGrid = gbm_grid, verbose = FALSE)

cat("[3/3] Training Penalized Linear Regression (LASSO/Ridge/Elastic Net)...\n")
model_reg_glmnet <- train(salary ~ ., data = regTrain, method = "glmnet", 
                          trControl = reg_control, tuneGrid = glmnet_grid)

# Compare Regression Models on TEST set
cat("\nEvaluating models on 20% Test Set...\n")
eval_reg_model <- function(model, name) {
  preds <- predict(model, regTest)
  rmse <- sqrt(mean((preds - regTest$salary)^2))
  return(data.frame(Model = name, RMSE = rmse))
}

results_reg <- rbind(
  eval_reg_model(model_lm, "Linear_Regression"),
  eval_reg_model(model_reg_gbm, "GBM"),
  eval_reg_model(model_reg_glmnet, "GLMNET")
)
print(results_reg)

# Find the best model based on Lowest RMSE
best_reg_name <- results_reg$Model[which.min(results_reg$RMSE)]
cat(sprintf("\n🏆 BEST REGRESSION MODEL: %s\n", best_reg_name))

# Save Multiple Linear Regression Model for Salary Prediction (fully trimmed to <50KB)
salary_model_path <- "models/salary_model_R.rds"
if (!dir.exists("models")) dir.create("models", recursive = TRUE)
model_lm$trainingData <- NULL
if (!is.null(model_lm$finalModel)) {
  model_lm$finalModel$residuals <- NULL
  model_lm$finalModel$fitted.values <- NULL
  model_lm$finalModel$model <- NULL
  model_lm$finalModel$weights <- NULL
  model_lm$finalModel$effects <- NULL
  model_lm$finalModel$qr$qr <- NULL
}
saveRDS(model_lm, salary_model_path, compress = "gzip")
cat(sprintf("[+] Multiple Linear Regression Salary Model successfully saved to: %s\n", salary_model_path))


# ==============================================================================
# 3. TEST PREDICTION ON NEW APPLICANT (USING RANDOM FOREST & LINEAR REGRESSION)
# ==============================================================================
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

for (col in names(sample_student)) {
  if (is.factor(dataTrain[[col]])) {
    sample_student[[col]] <- factor(sample_student[[col]], levels = levels(dataTrain[[col]]))
  }
}

# Random Forest classification prediction
employment_pred <- predict(model_rf, sample_student)
employment_prob <- predict(model_rf, sample_student, type = "prob")[1, "Employed"]

# Multiple Linear Regression prediction
salary_pred <- predict(model_lm, sample_student)

cat(sprintf("Predicted Status: %s (Probability of being employed: %.2f%%)\n", 
            as.character(employment_pred), employment_prob * 100))
if (employment_pred == "Employed") {
  cat(sprintf("Estimated Starting Salary: $%.2f\n", salary_pred))
}
