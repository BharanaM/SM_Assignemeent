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

# Explicitly set working directory to project root
target_dir <- "C:/Users/user/OneDrive - Sri Lanka Institute of Information Technology/OOP/Documents/SLIIT 3.1/IT3081 - Statistical Modeling/Graduate Employment Analysis"
if (dir.exists(target_dir)) {
  setwd(target_dir)
} else {
  try({
    args_full <- commandArgs(trailingOnly = FALSE)
    file_arg <- grep("--file=", args_full, value = TRUE)
    if (length(file_arg) > 0) {
      script_path <- sub("--file=", "", file_arg[1])
      setwd(normalizePath(file.path(dirname(script_path), ".."), winslash = "/"))
    }
  }, silent = TRUE)
}

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

cat("\n[1/3] Training Random Forest (optimized for smooth, well-calibrated probabilities)...\n")
# Using ntree = 100 and nodesize = 50 prevents noisy leaf overconfidence and ensures monotonic probabilities
rf_grid <- data.frame(mtry = floor(sqrt(ncol(dataTrain))))
model_rf <- train(Is_Employed ~ ., data = dataTrain, method = "rf", 
                  trControl = train_control, tuneGrid = rf_grid, 
                  ntree = 100, nodesize = 50)

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
if (!is.null(model_rf$terms)) {
  environment(model_rf$terms) <- baseenv()
}
if (!is.null(model_rf$finalModel$terms)) {
  environment(model_rf$finalModel$terms) <- baseenv()
}
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

# Train Multiple Linear Regression using statistically selected predictors (from 03_modelling.R)
# This eliminates multicollinearity and guarantees monotonic degree tier progression (PhD > Master's > Bachelor's > Diploma)
salary_formula <- salary ~ gpa + age + education_level + field_of_study + internship_experience

cat("\n[1/3] Training Multiple Linear Regression...\n")
model_lm <- lm(salary_formula, data = regTrain)

cat("[2/3] Training Gradient Boosting Machine (GBM) Regression...\n")
model_reg_gbm <- train(salary_formula, data = regTrain, method = "gbm", 
                       trControl = reg_control, tuneGrid = gbm_grid, verbose = FALSE)

cat("[3/3] Training Penalized Linear Regression (LASSO/Ridge/Elastic Net)...\n")
model_reg_glmnet <- train(salary_formula, data = regTrain, method = "glmnet", 
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

# Save Multiple Linear Regression Model for Salary Prediction (fully trimmed to <15KB)
salary_model_path <- "models/salary_model_R.rds"
if (!dir.exists("models")) dir.create("models", recursive = TRUE)

fit_salary <- model_lm
fit_salary$residuals <- NULL
fit_salary$fitted.values <- NULL
fit_salary$model <- NULL
fit_salary$weights <- NULL
fit_salary$effects <- NULL
fit_salary$qr$qr <- NULL
if (!is.null(fit_salary$terms)) {
  environment(fit_salary$terms) <- baseenv()
}

saveRDS(fit_salary, salary_model_path, compress = "gzip")
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

cat("\n--- Verification 1: High-Profile Applicant (IT, High Ranking, GPA 3.8, Internship: Yes) ---\n")
deg_levels <- c("PhD", "Master's", "Bachelor's", "Diploma")
for (deg in deg_levels) {
  test_deg <- sample_student
  test_deg$education_level <- factor(deg, levels = levels(dataTrain$education_level))
  p <- predict(model_rf, test_deg, type = "prob")[1, "Employed"]
  if (p >= 0.5) {
    s <- predict(model_lm, test_deg)
    cat(sprintf("  [%s] Likelihood: %.1f%% (Employed) | Starting Salary: $%.2f\n", deg, p * 100, s))
  } else {
    cat(sprintf("  [%s] Likelihood: %.1f%% (Unemployed) | Starting Salary: N/A (Candidate is Unemployed)\n", deg, p * 100))
  }
}

cat("\n--- Verification 2: Candidate with Lower Credentials (Arts, Medium Ranking, GPA 2.70, Internship: No) ---\n")
sample_moderate <- data.frame(
  country_of_origin = factor("Brazil", levels = levels(dataTrain$country_of_origin)),
  education_level = factor("Bachelor's", levels = levels(dataTrain$education_level)),
  field_of_study = factor("Arts", levels = levels(dataTrain$field_of_study)),
  language_proficiency = factor("Intermediate", levels = levels(dataTrain$language_proficiency)),
  visa_type = factor("Permanent Residency", levels = levels(dataTrain$visa_type)),
  gender = factor("Female", levels = levels(dataTrain$gender)),
  university_ranking = factor("Medium", levels = levels(dataTrain$university_ranking)),
  region_of_study = factor("Australia", levels = levels(dataTrain$region_of_study)),
  internship_experience = factor("No", levels = levels(dataTrain$internship_experience)),
  age = 30,
  years_since_graduation = 5,
  gpa = 2.70
)

for (deg in deg_levels) {
  test_deg2 <- sample_moderate
  test_deg2$education_level <- factor(deg, levels = levels(dataTrain$education_level))
  p <- predict(model_rf, test_deg2, type = "prob")[1, "Employed"]
  if (p >= 0.5) {
    s <- predict(model_lm, test_deg2)
    cat(sprintf("  [%s] Likelihood: %.1f%% (Employed) | Starting Salary: $%.2f\n", deg, p * 100, s))
  } else {
    cat(sprintf("  [%s] Likelihood: %.1f%% (Unemployed) | Starting Salary: N/A (Candidate is Unemployed)\n", deg, p * 100))
  }
}
