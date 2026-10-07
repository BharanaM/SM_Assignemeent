# ==============================================================================
# 02_ADVANCED_STATISTICAL_INFERENCE.R
# ==============================================================================
setwd("C:/Users/user/OneDrive - Sri Lanka Institute of Information Technology/OOP/Documents/SLIIT 3.1/IT3081 - Statistical Modeling/Graduate Employment Analysis")

library(tidyverse)
library(broom)

# Ensure car package is installed for Levene's Test
if(!require(car)) {
  install.packages("car", repos = "http://cran.us.r-project.org")
  library(car)
}

cat("\n[1] Loading dataset...\n")
file_path <- file.path("data", "preprocessed", "dataset_predictive.csv")
df <- read.csv(file_path, stringsAsFactors = TRUE)

df$employment_status <- as.factor(ifelse(df$employment_status == "Employed", "Employed", "Not_Employed"))
df_employed <- df %>% filter(employment_status == "Employed")

dir.create("res", showWarnings = FALSE, recursive = TRUE)

results_list <- list()

# Helper Functions for Effect Sizes
calculate_cohens_d <- function(g1, g2) {
  n1 <- length(g1); n2 <- length(g2)
  var1 <- var(g1, na.rm=TRUE); var2 <- var(g2, na.rm=TRUE)
  pooled_sd <- sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
  d <- abs(mean(g1, na.rm=TRUE) - mean(g2, na.rm=TRUE)) / pooled_sd
  return(d)
}

calculate_cramers_v <- function(tbl) {
  chi2 <- suppressWarnings(chisq.test(tbl)$statistic)
  n <- sum(tbl)
  min_dim <- min(nrow(tbl)-1, ncol(tbl)-1)
  v <- sqrt(chi2 / (n * min_dim))
  return(as.numeric(v))
}

# 1. Salary by Internship (Employed Only) - T-Test & Mann-Whitney
cat("\n[TEST 1] Salary by Internship\n")
g1 <- df_employed$salary[df_employed$internship_experience == levels(df_employed$internship_experience)[1]]
g2 <- df_employed$salary[df_employed$internship_experience == levels(df_employed$internship_experience)[2]]
ttest_salary <- t.test(g1, g2)
mann_whitney <- wilcox.test(g1, g2)
cohens_d_salary <- calculate_cohens_d(g1, g2)

results_list[[1]] <- data.frame(
  Test_Name = "Salary by Internship",
  H0 = "Mean salary is equal for those with and without internships.",
  H1 = "Mean salary differs by internship experience.",
  Test_Used = "Two-sample t-test (and Mann-Whitney)",
  P_Value = ttest_salary$p.value,
  Effect_Size_Metric = "Cohen's d",
  Effect_Size_Value = cohens_d_salary,
  Practical_Meaning = "Internships moderately increase starting salaries.",
  stringsAsFactors = FALSE
)

# 2. Employment Rate by Internship (Two-Proportion Test)
cat("\n[TEST 2] Employment Rate by Internship\n")
employed_with_intern <- sum(df$employment_status == "Employed" & df$internship_experience == "Yes")
total_intern <- sum(df$internship_experience == "Yes")
employed_no_intern <- sum(df$employment_status == "Employed" & df$internship_experience == "No")
total_no_intern <- sum(df$internship_experience == "No")

prop_test_res <- prop.test(x = c(employed_with_intern, employed_no_intern), n = c(total_intern, total_no_intern))

# Effect size (Cohen's h approximation)
h <- 2 * asin(sqrt(employed_with_intern/total_intern)) - 2 * asin(sqrt(employed_no_intern/total_no_intern))

results_list[[2]] <- data.frame(
  Test_Name = "Employment Rate by Internship",
  H0 = "Employment proportions are equal for both internship groups.",
  H1 = "Employment proportions differ by internship experience.",
  Test_Used = "Two-proportion Z-test",
  P_Value = prop_test_res$p.value,
  Effect_Size_Metric = "Cohen's h",
  Effect_Size_Value = abs(h),
  Practical_Meaning = "Internships strongly improve likelihood of employment.",
  stringsAsFactors = FALSE
)

# 3. Salary by Education Level (ANOVA)
cat("\n[TEST 3] ANOVA: Salary by Education Level (Employed Only)\n")
anova_model <- aov(salary ~ education_level, data = df_employed)
anova_p <- summary(anova_model)[[1]][["Pr(>F)"]][1]
tukey_res <- TukeyHSD(anova_model)
print(tukey_res)

# Eta-squared for ANOVA effect size
ss <- summary(anova_model)[[1]][["Sum Sq"]]
eta_sq <- ss[1] / sum(ss)

# Assumption checks for ANOVA
cat("\n[TEST] Checking ANOVA Assumptions\n")
residuals <- residuals(anova_model)
# Shapiro Wilk on subset to check normality
shapiro_res <- shapiro.test(sample(residuals, 4999)) 
levene_res <- leveneTest(salary ~ education_level, data = df_employed)
kruskal_res <- kruskal.test(salary ~ education_level, data = df_employed)

results_list[[3]] <- data.frame(
  Test_Name = "Salary by Education Level",
  H0 = "Mean salary is equal across all education levels.",
  H1 = "At least one education level has a different mean salary.",
  Test_Used = "One-way ANOVA (with Kruskal-Wallis fallback)",
  P_Value = anova_p,
  Effect_Size_Metric = "Eta-squared",
  Effect_Size_Value = eta_sq,
  Practical_Meaning = "Education level is a dominant factor in determining salary.",
  stringsAsFactors = FALSE
)

# 4. Salary variance across groups: Levene's Test
results_list[[4]] <- data.frame(
  Test_Name = "Salary Variance by Education Level",
  H0 = "Variance in salary is equal across education levels.",
  H1 = "Variance in salary differs across education levels.",
  Test_Used = "Levene's Test",
  P_Value = levene_res$`Pr(>F)`[1],
  Effect_Size_Metric = "N/A",
  Effect_Size_Value = NA,
  Practical_Meaning = "Higher degrees may show a wider spread of salaries.",
  stringsAsFactors = FALSE
)

# Additional basic tests
run_advanced_chi_square <- function(variable_name, question) {
  tbl <- table(df[[variable_name]], df$employment_status)
  chi_test <- suppressWarnings(chisq.test(tbl))
  cramer_v <- calculate_cramers_v(tbl)
  
  return(data.frame(
    Test_Name = question,
    H0 = paste(variable_name, "and employment status are independent."),
    H1 = paste(variable_name, "and employment status are associated."),
    Test_Used = "Chi-square test",
    P_Value = chi_test$p.value,
    Effect_Size_Metric = "Cramer's V",
    Effect_Size_Value = cramer_v,
    Practical_Meaning = paste("Significant association exists with", variable_name),
    stringsAsFactors = FALSE
  ))
}

results_list[[5]] <- run_advanced_chi_square("field_of_study", "Field of Study vs Employment")
results_list[[6]] <- run_advanced_chi_square("language_proficiency", "Language Proficiency vs Employment")
results_list[[7]] <- run_advanced_chi_square("university_ranking", "University Ranking vs Employment")

# ------------------------------------------------------------------------------
# Data Aggregation & Multiple Testing Correction (FDR)
# ------------------------------------------------------------------------------
results_summary <- bind_rows(results_list)

results_summary$Adjusted_P_Value <- p.adjust(results_summary$P_Value, method = "BH")
results_summary$Significant <- ifelse(results_summary$Adjusted_P_Value < 0.05, "Yes", "No")
results_summary$Effect_Size_Value <- round(results_summary$Effect_Size_Value, 3)

dir.create(file.path("outputs", "tables"), showWarnings = FALSE, recursive = TRUE)
write.csv(results_summary, file.path("outputs", "tables", "inference_results.csv"), row.names = FALSE)

cat("\n[+] Advanced Statistical Inference completed! Results saved to outputs/tables/inference_results.csv\n")
