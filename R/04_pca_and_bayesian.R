# ==============================================================================
# 04_PCA_AND_BAYESIAN.R
# ==============================================================================
setwd("C:/Users/user/OneDrive - Sri Lanka Institute of Information Technology/OOP/Documents/SLIIT 3.1/IT3081 - Statistical Modeling/Graduate Employment Analysis")

# Install necessary packages
packages <- c("tidyverse", "caret", "e1071", "rstanarm", "MCMCpack", "janitor")
new_packages <- packages[!(packages %in% installed.packages()[,"Package"])]
if(length(new_packages)) install.packages(new_packages, repos="http://cran.us.r-project.org")

library(tidyverse)
library(janitor)
library(caret)
library(e1071)
library(rstanarm)

cat("\n[1] Loading Preprocessed Data...\n")
file_path <- file.path("data", "preprocessed", "dataset_predictive.csv")
df <- read.csv(file_path, stringsAsFactors = TRUE)

df_emp <- df %>% 
  mutate(target = as.factor(ifelse(employment_status == "Employed", 1, 0))) %>%
  dplyr::select(-employment_status, -salary, -job_sector)

dir.create(file.path("outputs", "tables"), showWarnings = FALSE, recursive = TRUE)
dir.create(file.path("outputs", "figures"), showWarnings = FALSE, recursive = TRUE)

# ==============================================================================
# TASK 7: PRINCIPAL COMPONENT ANALYSIS (PCA)
# ==============================================================================
cat("\n[+] Running Principal Component Analysis...\n")

# Select only numeric continuous variables
df_numeric <- df_emp %>% dplyr::select(age, years_since_graduation, gpa)

# Correlation Matrix
cor_matrix <- cor(df_numeric, use = "complete.obs")
write.csv(as.data.frame(cor_matrix), file.path("outputs", "tables", "pca_correlation_matrix.csv"))

# Run PCA
pca_res <- prcomp(df_numeric, scale. = TRUE)

# Cumulative Variance and Loadings
pca_summary <- summary(pca_res)
write.csv(as.data.frame(pca_summary$importance), file.path("outputs", "tables", "pca_variance.csv"))
write.csv(as.data.frame(pca_res$rotation), file.path("outputs", "tables", "pca_loadings.csv"))

# Kaiser Criterion (Eigenvalues > 1)
eigenvalues <- pca_res$sdev^2
cat("\nEigenvalues (Kaiser Criterion):\n")
print(eigenvalues)

# PCA-based Logistic Regression vs Original variables
set.seed(42)
sample_idx <- sample(1:nrow(df_numeric), 5000)

# Original model
orig_glm <- glm(target ~ age + years_since_graduation + gpa, data = df_emp[sample_idx,], family = binomial)

# PCR model
pca_data <- as.data.frame(pca_res$x[sample_idx, ])
pca_data$target <- df_emp$target[sample_idx]
pcr_glm <- glm(target ~ PC1 + PC2 + PC3, data = pca_data, family = binomial)

cat("\n[+] PCA Analysis Complete (Data exported to outputs/tables/)\n")


# ==============================================================================
# TASK 8: BAYESIAN METHODS
# ==============================================================================
cat("\n[+] Running Bayesian Methods...\n")

set.seed(42)
trainIndex <- createDataPartition(df_emp$target, p = 0.8, list = FALSE)
train_data <- df_emp[trainIndex, ]
test_data <- df_emp[-trainIndex, ]

# 1. Naive Bayes ---------------------------------------------------------------
cat("\n[-] Training Naive Bayes...\n")
nb_model <- naiveBayes(target ~ ., data = train_data)

probs_nb <- predict(nb_model, test_data, type = "raw")[,2]
preds_nb <- predict(nb_model, test_data)

cm_nb <- confusionMatrix(preds_nb, test_data$target, positive="1")
roc_obj_nb <- pROC::roc(test_data$target, probs_nb, quiet=TRUE)
auc_val_nb <- as.numeric(pROC::auc(roc_obj_nb))

nb_results <- data.frame(
  Model = "Naive Bayes",
  Accuracy = cm_nb$overall["Accuracy"],
  Precision = cm_nb$byClass["Pos Pred Value"],
  Recall = cm_nb$byClass["Sensitivity"],
  F1_Score = cm_nb$byClass["F1"],
  AUC = auc_val_nb
)

# Append to previous model comparison
comp_path <- file.path("outputs", "tables", "model_comparison.csv")
if(file.exists(comp_path)) {
  prev_comp <- read.csv(comp_path)
  new_comp <- rbind(prev_comp, nb_results)
  write.csv(new_comp, comp_path, row.names = FALSE)
  cat("\n[-] Naive Bayes results appended to model_comparison.csv\n")
}

# 2. Bayesian Logistic Regression (rstanarm) -----------------------------------
cat("\n[-] Running Bayesian Logistic Regression (rstanarm) on a random sample of 1,000 rows...\n")
# Using a small sample and short chains because Bayesian MCMC on 240,000 rows takes hours
train_sample <- train_data[sample(nrow(train_data), 1000), ]

stan_mod <- stan_glm(
  target ~ gpa + internship_experience + university_ranking, 
  data = train_sample, 
  family = binomial(link = "logit"),
  prior = normal(0, 2.5),
  chains = 2,
  iter = 1000,
  refresh = 0
)

stan_summary <- summary(stan_mod, probs = c(0.025, 0.975)) # 95% Credible Intervals
write.csv(as.data.frame(stan_summary), file.path("outputs", "tables", "bayesian_regression_posterior.csv"))

# 3. Bayesian Decision Example: Beta-Binomial for Internship Effectiveness ------
cat("\n[-] Calculating Beta-Binomial Posterior for Internship...\n")
# Calculate successes (employed) and trials (total) for both groups
success_intern <- sum(df$employment_status == "Employed" & df$internship_experience == "Yes")
trials_intern <- sum(df$internship_experience == "Yes")

success_no_intern <- sum(df$employment_status == "Employed" & df$internship_experience == "No")
trials_no_intern <- sum(df$internship_experience == "No")

# Assuming uniform prior Beta(1,1)
# Posterior = Beta(1 + successes, 1 + trials - successes)
alpha_intern <- 1 + success_intern
beta_intern <- 1 + trials_intern - success_intern

alpha_no_intern <- 1 + success_no_intern
beta_no_intern <- 1 + trials_no_intern - success_no_intern

# Simulation to find probability that internship group has higher employment rate
n_sims <- 100000
post_intern <- rbeta(n_sims, alpha_intern, beta_intern)
post_no_intern <- rbeta(n_sims, alpha_no_intern, beta_no_intern)

prob_intern_better <- mean(post_intern > post_no_intern)

bayesian_decision <- data.frame(
  Metric = c("Posterior Mean (Internship)", "Posterior Mean (No Internship)", "Prob(Internship > No Internship)"),
  Value = c(mean(post_intern), mean(post_no_intern), prob_intern_better)
)

write.csv(bayesian_decision, file.path("outputs", "tables", "bayesian_decision_example.csv"), row.names=FALSE)
cat("\n[+] PCA and Bayesian Methods Pipeline Completed!\n")
