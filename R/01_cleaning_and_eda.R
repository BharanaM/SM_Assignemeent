library(here)
setwd("C:/Users/user/OneDrive - Sri Lanka Institute of Information Technology/OOP/Documents/SLIIT 3.1/IT3081 - Statistical Modeling/Graduate Employment Analysis")
# Loading packages
library(tidyverse)
library(janitor)
library(skimr)
library(scales)

# Importing the data
df <- read_csv("C:/Users/user/OneDrive - Sri Lanka Institute of Information Technology/OOP/Documents/SLIIT 3.1/IT3081 - Statistical Modeling/Graduate Employment Analysis/data/raw/dataset_predictive.csv") %>%
  clean_names()

cat("Original number of rows:", nrow(df), "\n")
cat("Original number of columns:", ncol(df), "\n")

# Basic data structure
cat("\n================ DATA STRUCTURE ================\n")
print(names(df))
cat("\n\nStructure:\n")
glimpse(df)

# Handling duplicates
duplicate_count <- sum(duplicated(df))

cat(
  "\nNumber of duplicate rows:",
  duplicate_count,
  "\n"
)

df_clean <- df %>%
  distinct()

cat(
  "\nRows after removing duplicates:",
  nrow(df_clean),
  "\n"
)

cat(
  "Remaining duplicate rows:",
  sum(duplicated(df_clean)),
  "\n"
)

dir.create(file.path("data", "preprocessed"), recursive = TRUE, showWarnings = FALSE)
write_csv(
  df_clean,
  file.path("data", "preprocessed", "dataset_predictive.csv")
)

# converting categorical variables to the factors
categorical_variables <- c(
  "country_of_origin",
  "education_level",
  "field_of_study",
  "language_proficiency",
  "visa_type",
  "gender",
  "university_ranking",
  "region_of_study",
  "internship_experience",
  "employment_status",
  "job_sector"
)

df_clean <- df_clean %>%
  mutate(
    across(
      all_of(categorical_variables),
      as.factor
    )
  )

# checking variables after conversion
cat("\n================ VARIABLE TYPES ================\n")

str(df_clean)


# dataset summary
dataset_summary <- tibble(
  original_rows = nrow(df),
  duplicate_rows = duplicate_count,
  final_rows = nrow(df_clean),
  columns = ncol(df_clean),
  missing_values = sum(is.na(df_clean))
)

print(dataset_summary)

write_csv(
  dataset_summary,
  file.path("outputs", "tables", "dataset_summary.csv")
)

# Saving category frequences
for (variable in categorical_variables) {
  
  frequency_table <- df_clean %>%
    count(.data[[variable]], sort = TRUE) %>%
    mutate(
      percentage = round(
        n / sum(n) * 100,
        2
      )
    )
  
  write_csv(
    frequency_table,
    paste0(
      file.path("outputs", "tables", ""),
      variable,
      "_frequency.csv"
    )
  )
}

# Numerical variable summary
numeric_summary <- df_clean %>%
  summarise(
    across(
      c(
        age,
        years_since_graduation,
        gpa,
        salary
      ),
      list(
        mean = ~ mean(.x, na.rm = TRUE),
        median = ~ median(.x, na.rm = TRUE),
        sd = ~ sd(.x, na.rm = TRUE),
        minimum = ~ min(.x, na.rm = TRUE),
        maximum = ~ max(.x, na.rm = TRUE),
        q1 = ~ quantile(.x, 0.25, na.rm = TRUE),
        q3 = ~ quantile(.x, 0.75, na.rm = TRUE)
      )
    )
  )

print(numeric_summary)

write_csv(
  numeric_summary,
  file.path("outputs", "tables", "numerical_summary.csv")
)

# Employment status summary
employment_summary <- df_clean %>%
  count(
    employment_status,
    sort = TRUE
  ) %>%
  mutate(
    percentage = round(
      n / sum(n) * 100,
      2
    )
  )

print(employment_summary)

write_csv(
  employment_summary,
  file.path("outputs", "tables", "employment_summary.csv")
)


# Employment status bar chart
p_employment <- ggplot(
  employment_summary,
  aes(
    x = employment_status,
    y = n
  )
) +
  geom_col() +
  geom_text(
    aes(
      label = paste0(
        comma(n),
        "\n",
        percentage,
        "%"
      )
    ),
    vjust = -0.3,
    size = 4
  ) +
  labs(
    title = "Distribution of Graduate Employment Status",
    x = "Employment Status",
    y = "Number of Graduates"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(
      face = "bold"
    )
  )

print(p_employment)

ggsave(
  file.path("outputs", "figures", "employment_status.png"),
  p_employment,
  width = 9,
  height = 6,
  dpi = 300
)


# Education level distribution
education_summary <- df_clean %>%
  count(
    education_level,
    sort = TRUE
  ) %>%
  mutate(
    percentage = n / sum(n) * 100
  )

print(education_summary)

write_csv(
  education_summary,
  file.path("outputs", "tables", "education_summary.csv")
)
p_education <- ggplot(
  education_summary,
  aes(
    x = reorder(education_level, n),
    y = n
  )
) +
  geom_col() +
  geom_text(
    aes(
      label = paste0(
        comma(n),
        "\n",
        round(percentage, 1),
        "%"
      )
    ),
    vjust = -0.3,
    size = 3.5
  ) +
  labs(
    title = "Distribution of Education Levels",
    x = "Education Level",
    y = "Number of Graduates"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(
      angle = 30,
      hjust = 1
    )
  )

print(p_education)

ggsave(
  file.path("outputs", "figures", "education_level.png"),
  p_education,
  width = 9,
  height = 6,
  dpi = 300
)


# Field of study distribution
field_summary <- df_clean %>%
  count(
    field_of_study,
    sort = TRUE
  ) %>%
  mutate(
    percentage = n / sum(n) * 100
  )

print(field_summary)

write_csv(
  field_summary,
  file.path("outputs", "tables", "field_of_study_summary.csv")
)
p_field <- ggplot(
  field_summary,
  aes(
    x = reorder(field_of_study, n),
    y = n
  )
) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Distribution of Graduates by Field of Study",
    x = "Field of Study",
    y = "Number of Graduates"
  ) +
  theme_minimal()

print(p_field)
ggsave(
  file.path("outputs", "figures", "field_of_study.png"),
  p_field,
  width = 9,
  height = 7,
  dpi = 300
)


# Country of origin
country_summary <- df_clean %>%
  count(
    country_of_origin,
    sort = TRUE
  ) %>%
  mutate(
    percentage = n / sum(n) * 100
  )

print(
  head(country_summary, 20)
)

write_csv(
  country_summary,
  file.path("outputs", "tables", "country_summary.csv")
)


# Language proficiency
language_summary <- df_clean %>%
  count(
    language_proficiency,
    sort = TRUE
  ) %>%
  mutate(
    percentage = n / sum(n) * 100
  )

print(language_summary)

write_csv(
  language_summary,
  file.path("outputs", "tables", "language_proficiency_summary.csv")
)
p_language <- ggplot(
  language_summary,
  aes(
    x = reorder(language_proficiency, n),
    y = n
  )
) +
  geom_col() +
  labs(
    title = "Distribution of Language Proficiency",
    x = "Language Proficiency",
    y = "Number of Graduates"
  ) +
  theme_minimal()

print(p_language)
ggsave(
  file.path("outputs", "figures", "language_proficiency.png"),
  p_language,
  width = 9,
  height = 6,
  dpi = 300
)


# Internship experience
internship_summary <- df_clean %>%
  count(
    internship_experience,
    sort = TRUE
  ) %>%
  mutate(
    percentage = n / sum(n) * 100
  )

print(internship_summary)

write_csv(
  internship_summary,
  file.path("outputs", "tables", "internship_summary.csv")
)
p_internship <- ggplot(
  internship_summary,
  aes(
    x = internship_experience,
    y = n
  )
) +
  geom_col() +
  geom_text(
    aes(
      label = paste0(
        comma(n),
        "\n",
        round(percentage, 1),
        "%"
      )
    ),
    vjust = -0.3
  ) +
  labs(
    title = "Graduate Internship Experience",
    x = "Internship Experience",
    y = "Number of Graduates"
  ) +
  theme_minimal()

print(p_internship)

ggsave(
  file.path("outputs", "figures", "internship_experience.png"),
  p_internship,
  width = 9,
  height = 6,
  dpi = 300
)


# GPA Distribution
p_gpa <- ggplot(
  df_clean,
  aes(x = gpa)
) +
  geom_histogram(
    bins = 30
  ) +
  labs(
    title = "Distribution of Graduate GPA",
    x = "GPA",
    y = "Frequency"
  ) +
  theme_minimal()

print(p_gpa)

ggsave(
  file.path("outputs", "figures", "gpa_distribution.png"),
  p_gpa,
  width = 9,
  height = 6,
  dpi = 300
)


# Age distribution
p_age <- ggplot(
  df_clean,
  aes(x = age)
) +
  geom_histogram(
    bins = 30
  ) +
  labs(
    title = "Distribution of Graduate Age",
    x = "Age",
    y = "Frequency"
  ) +
  theme_minimal()

print(p_age)

ggsave(
  file.path("outputs", "figures", "age_distribution.png"),
  p_age,
  width = 9,
  height = 6,
  dpi = 300
)

# Years since graduation
p_years <- ggplot(
  df_clean,
  aes(x = years_since_graduation)
) +
  geom_histogram(
    bins = 20
  ) +
  labs(
    title = "Distribution of Years Since Graduation",
    x = "Years Since Graduation",
    y = "Frequency"
  ) +
  theme_minimal()

print(p_years)

ggsave(
  file.path("outputs", "figures", "years_since_graduation.png"),
  p_years,
  width = 9,
  height = 6,
  dpi = 300
)

# Salary distribution
p_salary <- ggplot(
  df_clean,
  aes(x = salary)
) +
  geom_histogram(
    bins = 40
  ) +
  labs(
    title = "Distribution of Graduate Salary",
    x = "Salary",
    y = "Frequency"
  ) +
  theme_minimal()

print(p_salary)

ggsave(
  file.path("outputs", "figures", "salary_distribution.png"),
  p_salary,
  width = 9,
  height = 6,
  dpi = 300
)


# Salary BoxPlot
p_salary_box <- ggplot(
  df_clean,
  aes(y = salary)
) +
  geom_boxplot() +
  labs(
    title = "Boxplot of Graduate Salary",
    y = "Salary"
  ) +
  theme_minimal()

print(p_salary_box)

ggsave(
  file.path("outputs", "figures", "salary_boxplot.png"),
  p_salary_box,
  width = 7,
  height = 6,
  dpi = 300
)


# Employment status by internship experience
internship_employment <- df_clean %>%
  count(
    internship_experience,
    employment_status
  ) %>%
  group_by(internship_experience) %>%
  mutate(
    percentage = n / sum(n) * 100
  ) %>%
  ungroup()

print(internship_employment)

write_csv(
  internship_employment,
  file.path("outputs", "tables", "internship_employment.csv")
)

p_internship_employment <- ggplot(
  internship_employment,
  aes(
    x = internship_experience,
    y = percentage,
    fill = employment_status
  )
) +
  geom_col(
    position = "fill"
  ) +
  scale_y_continuous(
    labels = percent
  ) +
  labs(
    title = "Employment Status by Internship Experience",
    x = "Internship Experience",
    y = "Percentage"
  ) +
  theme_minimal()
print(p_internship_employment)

ggsave(
  file.path("outputs", "figures", "employment_by_internship.png"),
  p_internship_employment,
  width = 10,
  height = 6,
  dpi = 300
)


# GPA by employment status
gpa_employment_summary <- df_clean %>%
  group_by(employment_status) %>%
  summarise(
    n = n(),
    mean_gpa = mean(gpa, na.rm = TRUE),
    median_gpa = median(gpa, na.rm = TRUE),
    sd_gpa = sd(gpa, na.rm = TRUE),
    min_gpa = min(gpa, na.rm = TRUE),
    max_gpa = max(gpa, na.rm = TRUE),
    .groups = "drop"
  )

print(gpa_employment_summary)

write_csv(
  gpa_employment_summary,
  file.path("outputs", "tables", "gpa_by_employment.csv")
)
p_gpa_employment <- ggplot(
  df_clean,
  aes(
    x = employment_status,
    y = gpa
  )
) +
  geom_boxplot() +
  labs(
    title = "GPA Distribution by Employment Status",
    x = "Employment Status",
    y = "GPA"
  ) +
  theme_minimal()

print(p_gpa_employment)
ggsave(
  file.path("outputs", "figures", "gpa_by_employment.png"),
  p_gpa_employment,
  width = 9,
  height = 6,
  dpi = 300
)


# Age by employment status
age_employment_summary <- df_clean %>%
  group_by(employment_status) %>%
  summarise(
    n = n(),
    mean_age = mean(age, na.rm = TRUE),
    median_age = median(age, na.rm = TRUE),
    sd_age = sd(age, na.rm = TRUE),
    .groups = "drop"
  )

print(age_employment_summary)

write_csv(
  age_employment_summary,
  file.path("outputs", "tables", "age_by_employment.csv")
)
p_age_employment <- ggplot(
  df_clean,
  aes(
    x = employment_status,
    y = age
  )
) +
  geom_boxplot() +
  labs(
    title = "Age Distribution by Employment Status",
    x = "Employment Status",
    y = "Age"
  ) +
  theme_minimal()

print(p_age_employment)

ggsave(
  file.path("outputs", "figures", "age_by_employment.png"),
  p_age_employment,
  width = 9,
  height = 6,
  dpi = 300
)


# Years since graduation by employment status
years_employment_summary <- df_clean %>%
  group_by(employment_status) %>%
  summarise(
    n = n(),
    mean_years = mean(
      years_since_graduation,
      na.rm = TRUE
    ),
    median_years = median(
      years_since_graduation,
      na.rm = TRUE
    ),
    sd_years = sd(
      years_since_graduation,
      na.rm = TRUE
    ),
    .groups = "drop"
  )

print(years_employment_summary)

write_csv(
  years_employment_summary,
  file.path("outputs", "tables", "years_since_graduation_by_employment.csv")
)


p_years_employment <- ggplot(
  df_clean,
  aes(
    x = employment_status,
    y = years_since_graduation
  )
) +
  geom_boxplot() +
  labs(
    title = "Years Since Graduation by Employment Status",
    x = "Employment Status",
    y = "Years Since Graduation"
  ) +
  theme_minimal()

print(p_years_employment)

ggsave(
  file.path("outputs", "figures", "years_since_graduation_by_employment.png"),
  p_years_employment,
  width = 9,
  height = 6,
  dpi = 300
)


# Salary by employment status
salary_employment_summary <- df_clean %>%
  group_by(employment_status) %>%
  summarise(
    n = n(),
    mean_salary = mean(salary, na.rm = TRUE),
    median_salary = median(salary, na.rm = TRUE),
    sd_salary = sd(salary, na.rm = TRUE),
    min_salary = min(salary, na.rm = TRUE),
    max_salary = max(salary, na.rm = TRUE),
    .groups = "drop"
  )

print(salary_employment_summary)
write_csv(
  salary_employment_summary,
  file.path("outputs", "tables", "salary_by_employment.csv")
)


p_salary_employment <- ggplot(
  df_clean,
  aes(
    x = employment_status,
    y = salary
  )
) +
  geom_boxplot() +
  labs(
    title = "Salary Distribution by Employment Status",
    x = "Employment Status",
    y = "Salary"
  ) +
  theme_minimal()

print(p_salary_employment)

ggsave(
  file.path("outputs", "figures", "salary_by_employment.png"),
  p_salary_employment,
  width = 9,
  height = 6,
  dpi = 300
)


# Salary by education level
salary_education_summary <- df_clean %>%
  group_by(education_level) %>%
  summarise(
    n = n(),
    mean_salary = mean(salary, na.rm = TRUE),
    median_salary = median(salary, na.rm = TRUE),
    sd_salary = sd(salary, na.rm = TRUE),
    .groups = "drop"
  )

print(salary_education_summary)

write_csv(
  salary_education_summary,
  file.path("outputs", "tables", "salary_by_education.csv")
)


p_salary_education <- ggplot(
  df_clean,
  aes(
    x = education_level,
    y = salary
  )
) +
  geom_boxplot() +
  labs(
    title = "Salary Distribution by Education Level",
    x = "Education Level",
    y = "Salary"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(
      angle = 30,
      hjust = 1
    )
  )

print(p_salary_education)
ggsave(
  file.path("outputs", "figures", "salary_by_education.png"),
  p_salary_education,
  width = 10,
  height = 6,
  dpi = 300
)


# Salary by field of study
salary_field_summary <- df_clean %>%
  group_by(field_of_study) %>%
  summarise(
    n = n(),
    mean_salary = mean(salary, na.rm = TRUE),
    median_salary = median(salary, na.rm = TRUE),
    .groups = "drop"
  ) %>%
  arrange(desc(mean_salary))

print(salary_field_summary)

write_csv(
  salary_field_summary,
  file.path("outputs", "tables", "salary_by_field.csv")
)

p_salary_field <- ggplot(
  salary_field_summary,
  aes(
    x = reorder(field_of_study, mean_salary),
    y = mean_salary
  )
) +
  geom_col() +
  coord_flip() +
  labs(
    title = "Mean Salary by Field of Study",
    x = "Field of Study",
    y = "Mean Salary"
  ) +
  theme_minimal()

print(p_salary_field)

ggsave(
  file.path("outputs", "figures", "salary_by_field.png"),
  p_salary_field,
  width = 10,
  height = 7,
  dpi = 300
)



# Correlation matrix for numerical variables
numeric_data <- df_clean %>%
  select(
    age,
    years_since_graduation,
    gpa,
    salary
  )

correlation_matrix <- cor(
  numeric_data,
  use = "complete.obs"
)

print(
  round(
    correlation_matrix,
    3
  )
)
# Convert correlation matrix to a table
correlation_table <- as.data.frame(
  round(
    correlation_matrix,
    3
  )
)

write_csv(
  correlation_table,
  file.path("outputs", "tables", "correlation_matrix.csv")
)
s


cat("\n================ MISSING VALUE & OUTLIER ANALYSIS ================\n")

# 1. Missing Value Analysis
cat("\n[Missing Value Analysis]\n")
missing_by_status <- df_clean %>%
  group_by(employment_status) %>%
  summarise(
    missing_job_sector = sum(is.na(job_sector)),
    missing_salary = sum(is.na(salary) | salary == 0),
    total = n()
  )
print(missing_by_status)
cat("Note: Salary and Job Sector are NA/0 for Unemployed and Continuing Education graduates, which is structurally correct.\n")

# 2. Outlier Detection using IQR method
detect_outliers_iqr <- function(data, column) {
  q1 <- quantile(data[[column]], 0.25, na.rm = TRUE)
  q3 <- quantile(data[[column]], 0.75, na.rm = TRUE)
  iqr <- q3 - q1
  lower_bound <- q1 - 1.5 * iqr
  upper_bound <- q3 + 1.5 * iqr
  
  outliers <- data %>% filter(!!sym(column) < lower_bound | !!sym(column) > upper_bound)
  return(nrow(outliers))
}

outliers_summary <- data.frame(
  Variable = c("age", "years_since_graduation", "gpa", "salary"),
  Outliers_Count = c(
    detect_outliers_iqr(df_clean, "age"),
    detect_outliers_iqr(df_clean, "years_since_graduation"),
    detect_outliers_iqr(df_clean, "gpa"),
    detect_outliers_iqr(df_clean, "salary")
  )
)
print("\n[Outliers Detected (IQR Method)]")
print(outliers_summary)
write_csv(outliers_summary, file.path("outputs", "tables", "outliers_summary.csv"))

# 3. Correlation Heatmap
library(reshape2)
cormat <- round(cor(df_clean %>% select(age, years_since_graduation, gpa, salary), use="complete.obs"), 2)
melted_cormat <- melt(cormat)

p_heatmap <- ggplot(data = melted_cormat, aes(x=Var1, y=Var2, fill=value)) + 
  geom_tile() +
  scale_fill_gradient2(low = "blue", high = "red", mid = "white", midpoint = 0, limit = c(-1,1)) +
  geom_text(aes(Var1, Var2, label = value), color = "black", size = 4) +
  theme_minimal() + 
  labs(title="Correlation Heatmap of Numerical Variables")

print(p_heatmap)
ggsave(file.path("outputs", "figures", "correlation_heatmap.png"), p_heatmap, width=8, height=6, dpi=300)

cat("\nPhase 2 completed.\n")

# ==============================================================================
# ADDITIONAL DESCRIPTIVE ANALYSIS (Task 3 Requirements)
# ==============================================================================

# Ensure naniar is installed for missing plots
if(!require(naniar)) {
  install.packages("naniar", repos = "http://cran.us.r-project.org")
  library(naniar)
}

# 1. Salary handling: exclude zeros or NAs for unemployed graduates
cat("\n================ TASK 3: SALARY HANDLING ================\n")
df_employed <- df_clean %>%
  filter(employment_status == "Employed")

# Generate new salary summary excluding zeros
salary_summary_employed <- df_employed %>%
  summarise(
    mean_salary = mean(salary, na.rm = TRUE),
    median_salary = median(salary, na.rm = TRUE),
    sd_salary = sd(salary, na.rm = TRUE),
    min_salary = min(salary, na.rm = TRUE),
    max_salary = max(salary, na.rm = TRUE)
  )
print(salary_summary_employed)
write_csv(salary_summary_employed, file.path("outputs", "tables", "salary_summary_employed.csv"))

# 2. Outlier treatment decisions with boxplots for age and GPA
cat("\n================ TASK 3: OUTLIER BOXPLOTS ================\n")
p_age_outlier <- ggplot(df_clean, aes(y = age)) +
  geom_boxplot(fill = "lightblue") +
  labs(title = "Boxplot for Age", y = "Age") +
  theme_minimal()
print(p_age_outlier)
ggsave(file.path("outputs", "figures", "boxplot_age.png"), p_age_outlier, width = 6, height = 5)

p_gpa_outlier <- ggplot(df_clean, aes(y = gpa)) +
  geom_boxplot(fill = "lightgreen") +
  labs(title = "Boxplot for GPA", y = "GPA") +
  theme_minimal()
print(p_gpa_outlier)
ggsave(file.path("outputs", "figures", "boxplot_gpa.png"), p_gpa_outlier, width = 6, height = 5)

# 3. Missing plots: gender, visa type, region, university ranking and job sector
cat("\n================ TASK 3: MISSING PLOTS ================\n")
p_missing <- gg_miss_var(df_clean %>% select(gender, visa_type, region_of_study, university_ranking, job_sector)) +
  labs(title = "Missing Values by Selected Variables")
print(p_missing)
ggsave(file.path("outputs", "figures", "missing_plot.png"), p_missing, width = 8, height = 6)

# 4. Salary by gender, internship and job sector
cat("\n================ TASK 3: SALARY BY GROUPS ================\n")
p_salary_gender <- ggplot(df_employed, aes(x = gender, y = salary, fill = gender)) +
  geom_boxplot() +
  labs(title = "Salary Distribution by Gender (Employed Only)", x = "Gender", y = "Salary") +
  theme_minimal()
print(p_salary_gender)
ggsave(file.path("outputs", "figures", "salary_by_gender.png"), p_salary_gender, width = 8, height = 6)

p_salary_internship <- ggplot(df_employed, aes(x = internship_experience, y = salary, fill = internship_experience)) +
  geom_boxplot() +
  labs(title = "Salary Distribution by Internship Experience (Employed Only)", x = "Internship Experience", y = "Salary") +
  theme_minimal()
print(p_salary_internship)
ggsave(file.path("outputs", "figures", "salary_by_internship.png"), p_salary_internship, width = 8, height = 6)

p_salary_job_sector <- ggplot(df_employed, aes(x = reorder(job_sector, salary, FUN = median), y = salary, fill = job_sector)) +
  geom_boxplot() +
  coord_flip() +
  labs(title = "Salary Distribution by Job Sector (Employed Only)", x = "Job Sector", y = "Salary") +
  theme_minimal()
print(p_salary_job_sector)
ggsave(file.path("outputs", "figures", "salary_by_job_sector.png"), p_salary_job_sector, width = 10, height = 6)

# 5. Employment rate by field and region
cat("\n================ TASK 3: EMPLOYMENT RATES ================\n")
df_emp_rate_field <- df_clean %>%
  group_by(field_of_study) %>%
  summarise(employment_rate = mean(employment_status == "Employed") * 100)

p_emp_rate_field <- ggplot(df_emp_rate_field, aes(x = reorder(field_of_study, employment_rate), y = employment_rate)) +
  geom_col(fill = "steelblue") +
  coord_flip() +
  labs(title = "Employment Rate by Field of Study", x = "Field of Study", y = "Employment Rate (%)") +
  theme_minimal()
print(p_emp_rate_field)
ggsave(file.path("outputs", "figures", "emp_rate_by_field.png"), p_emp_rate_field, width = 9, height = 6)

df_emp_rate_region <- df_clean %>%
  group_by(region_of_study) %>%
  summarise(employment_rate = mean(employment_status == "Employed") * 100)

p_emp_rate_region <- ggplot(df_emp_rate_region, aes(x = reorder(region_of_study, employment_rate), y = employment_rate)) +
  geom_col(fill = "darkorange") +
  coord_flip() +
  labs(title = "Employment Rate by Region of Study", x = "Region of Study", y = "Employment Rate (%)") +
  theme_minimal()
print(p_emp_rate_region)
ggsave(file.path("outputs", "figures", "emp_rate_by_region.png"), p_emp_rate_region, width = 9, height = 6)

cat("\nTask 3 additional visualisations completed.\n")
