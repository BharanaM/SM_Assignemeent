# ==============================================================================
# 02_ADVANCED_STATISTICAL_INFERENCE.R
# This script performs highly rigorous statistical inference including:
# - Hypothesis Testing (Welch t-test, Chi-square)
# - Effect Size Calculations (Cohen's d, Cramer's V)
# - Multiple Testing Adjustments (Benjamini-Hochberg FDR)
# ==============================================================================

library(tidyverse)
library(broom)

cat("\n[1] Loading dataset...\n")
file_path <- "dataset_predictive.csv" 
df <- read.csv(file_path, stringsAsFactors = TRUE)

# Standardize Employment_Status to exactly 2 levels for the tests
df$Employment_Status <- as.factor(ifelse(df$Employment_Status == "Employed", "Employed", "Not_Employed"))

# Directory to save inference results
dir.create("res", showWarnings = FALSE, recursive = TRUE)

cat("\n======================================================\n")
cat("          ADVANCED STATISTICAL INFERENCE              \n")
cat("======================================================\n")

results_list <- list()

# ------------------------------------------------------------------------------
# Function 1: Manual Cohen's d for T-Test
# ------------------------------------------------------------------------------
calculate_cohens_d <- function(var_name, group_var) {
  g1 <- df[[var_name]][df[[group_var]] == levels(df[[group_var]])[1]]
  g2 <- df[[var_name]][df[[group_var]] == levels(df[[group_var]])[2]]
  
  n1 <- length(g1); n2 <- length(g2)
  var1 <- var(g1, na.rm=TRUE); var2 <- var(g2, na.rm=TRUE)
  
  pooled_sd <- sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
  d <- abs(mean(g1, na.rm=TRUE) - mean(g2, na.rm=TRUE)) / pooled_sd
  return(d)
}

# ------------------------------------------------------------------------------
# Function 2: Manual Cramer's V for Chi-Square
# ------------------------------------------------------------------------------
calculate_cramers_v <- function(tbl) {
  chi2 <- suppressWarnings(chisq.test(tbl)$statistic)
  n <- sum(tbl)
  min_dim <- min(nrow(tbl)-1, ncol(tbl)-1)
  v <- sqrt(chi2 / (n * min_dim))
  return(as.numeric(v))
}

# ------------------------------------------------------------------------------
# 1. Welch T-Test: GPA vs Employment Status
# ------------------------------------------------------------------------------
cat("\n[TEST 1] Welch t-test & Cohen's d: GPA\n")
ttest_gpa <- t.test(GPA ~ Employment_Status, data = df)
cohens_d <- calculate_cohens_d("GPA", "Employment_Status")

results_list[[1]] <- data.frame(
  Research_Question = "Is GPA associated with employment status?",
  Test_Used = "Welch t-test",
  P_Value = ttest_gpa$p.value,
  Effect_Size_Metric = "Cohen's d",
  Effect_Size_Value = cohens_d,
  stringsAsFactors = FALSE
)

# ------------------------------------------------------------------------------
# Helper function for Chi-Square tests with Cramer's V
# ------------------------------------------------------------------------------
run_advanced_chi_square <- function(variable_name, question) {
  cat(sprintf("\n[TEST] Chi-square & Cramer's V: %s\n", variable_name))
  tbl <- table(df[[variable_name]], df$Employment_Status)
  chi_test <- suppressWarnings(chisq.test(tbl))
  cramer_v <- calculate_cramers_v(tbl)
  
  return(data.frame(
    Research_Question = question,
    Test_Used = "Chi-square test",
    P_Value = chi_test$p.value,
    Effect_Size_Metric = "Cramer's V",
    Effect_Size_Value = cramer_v,
    stringsAsFactors = FALSE
  ))
}

results_list[[2]] <- run_advanced_chi_square("Education_Level", "Is education_level associated with employment status?")
results_list[[3]] <- run_advanced_chi_square("Field_of_Study", "Is field_of_study associated with employment status?")
results_list[[4]] <- run_advanced_chi_square("Language_Proficiency", "Is language_proficiency associated with employment status?")
results_list[[5]] <- run_advanced_chi_square("Internship_Experience", "Is internship_experience associated with employment status?")
results_list[[6]] <- run_advanced_chi_square("University_Ranking", "Is university_ranking associated with employment status?")

# ------------------------------------------------------------------------------
# Data Aggregation & Multiple Testing Correction (FDR)
# ------------------------------------------------------------------------------
results_summary <- bind_rows(results_list)

# Apply Benjamini-Hochberg False Discovery Rate (FDR) correction
results_summary$Adjusted_P_Value <- p.adjust(results_summary$P_Value, method = "BH")

# Format P-Values for presentation (prevents showing exactly '0')
format_pval <- function(p) {
  ifelse(p < 0.0001, "< 0.0001", sprintf("%.4f", p))
}

results_summary$Formatted_P_Value <- format_pval(results_summary$P_Value)
results_summary$Formatted_Adj_P_Value <- format_pval(results_summary$Adjusted_P_Value)

# Determine Significance based on Adjusted P-Value
results_summary$Significant <- ifelse(results_summary$Adjusted_P_Value < 0.05, "Yes", "No")

# Determine Effect Size Magnitude (Rules of Thumb)
get_effect_magnitude <- function(metric, value) {
  if (metric == "Cohen's d") {
    if (value >= 0.8) return("Large")
    if (value >= 0.5) return("Medium")
    if (value >= 0.2) return("Small")
    return("Negligible")
  } else {
    # Cramer's V thresholds
    if (value >= 0.25) return("Large")
    if (value >= 0.15) return("Medium")
    if (value >= 0.05) return("Small")
    return("Negligible")
  }
}

results_summary$Effect_Magnitude <- mapply(get_effect_magnitude, results_summary$Effect_Size_Metric, results_summary$Effect_Size_Value)

# Round effect size for display
results_summary$Effect_Size_Value <- round(results_summary$Effect_Size_Value, 3)

# ------------------------------------------------------------------------------
# Export Highly Advanced Summary
# ------------------------------------------------------------------------------
# Rearrange columns for Streamlit
final_export <- results_summary %>%
  select(
    Research_Question, 
    Test_Used, 
    Formatted_P_Value, 
    Formatted_Adj_P_Value, 
    Significant, 
    Effect_Size_Metric, 
    Effect_Size_Value, 
    Effect_Magnitude
  )

write.csv(final_export, "res/all_results.csv", row.names = FALSE)
cat("\n[+] Advanced Statistical Inference completed! Results saved to res/all_results.csv\n")
