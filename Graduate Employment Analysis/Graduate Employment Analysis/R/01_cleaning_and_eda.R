# Loading packages
library(tidyverse)
library(janitor)
library(skimr)
library(scales)

# Importing the data
df <- read_csv("data/dataset.csv") %>%
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

write_csv(
  df_clean,
  "data/cleaned_graduate_employment_data.csv"
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
  "outputs/tables/dataset_summary.csv"
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
      "outputs/tables/",
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
  "outputs/tables/numerical_summary.csv"
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
  "outputs/tables/employment_summary.csv"
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
  "outputs/figures/employment_status.png",
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
  "outputs/tables/education_summary.csv"
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
  "outputs/figures/education_level.png",
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
  "outputs/tables/field_of_study_summary.csv"
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
  "outputs/figures/field_of_study.png",
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
  "outputs/tables/country_summary.csv"
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
  "outputs/tables/language_proficiency_summary.csv"
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
  "outputs/figures/language_proficiency.png",
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
  "outputs/tables/internship_summary.csv"
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
  "outputs/figures/internship_experience.png",
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
  "outputs/figures/gpa_distribution.png",
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
  "outputs/figures/age_distribution.png",
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
  "outputs/figures/years_since_graduation.png",
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
  "outputs/figures/salary_distribution.png",
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
  "outputs/figures/salary_boxplot.png",
  p_salary_box,
  width = 7,
  height = 6,
  dpi = 300
)

# Employment status by education level
education_employment <- df_clean %>%
  count(
    education_level,
    employment_status
  ) %>%
  group_by(education_level) %>%
  mutate(
    percentage = n / sum(n) * 100
  ) %>%
  ungroup()

print(education_employment)

write_csv(
  education_employment,
  "outputs/tables/education_employment.csv"
)
p_education_employment <- ggplot(
  education_employment,
  aes(
    x = education_level,
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
    title = "Employment Status by Education Level",
    x = "Education Level",
    y = "Percentage"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(
      angle = 30,
      hjust = 1
    )
  )

print(p_education_employment)

ggsave(
  "outputs/figures/employment_by_education.png",
  p_education_employment,
  width = 10,
  height = 6,
  dpi = 300
)


# Employment status by field of study
field_employment <- df_clean %>%
  count(
    field_of_study,
    employment_status
  ) %>%
  group_by(field_of_study) %>%
  mutate(
    percentage = n / sum(n) * 100
  ) %>%
  ungroup()

write_csv(
  field_employment,
  "outputs/tables/field_employment.csv"
)


p_field_employment <- ggplot(
  field_employment,
  aes(
    x = field_of_study,
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
    title = "Employment Status by Field of Study",
    x = "Field of Study",
    y = "Percentage"
  ) +
  theme_minimal() +
  theme(
    axis.text.x = element_text(
      angle = 30,
      hjust = 1
    )
  )

print(p_field_employment)
ggsave(
  "outputs/figures/employment_by_field.png",
  p_field_employment,
  width = 11,
  height = 6,
  dpi = 300
)


# Employment status by language proficiency
language_employment <- df_clean %>%
  count(
    language_proficiency,
    employment_status
  ) %>%
  group_by(language_proficiency) %>%
  mutate(
    percentage = n / sum(n) * 100
  ) %>%
  ungroup()

print(language_employment)

write_csv(
  language_employment,
  "outputs/tables/language_employment.csv"
)
p_language_employment <- ggplot(
  language_employment,
  aes(
    x = language_proficiency,
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
    title = "Employment Status by Language Proficiency",
    x = "Language Proficiency",
    y = "Percentage"
  ) +
  theme_minimal()
print(p_language_employment)

ggsave(
  "outputs/figures/employment_by_language.png",
  p_language_employment,
  width = 10,
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
  "outputs/tables/internship_employment.csv"
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
  "outputs/figures/employment_by_internship.png",
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
  "outputs/tables/gpa_by_employment.csv"
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
  "outputs/figures/gpa_by_employment.png",
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
  "outputs/tables/age_by_employment.csv"
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
  "outputs/figures/age_by_employment.png",
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
  "outputs/tables/years_since_graduation_by_employment.csv"
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
  "outputs/figures/years_since_graduation_by_employment.png",
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
  "outputs/tables/salary_by_employment.csv"
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
  "outputs/figures/salary_by_employment.png",
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
  "outputs/tables/salary_by_education.csv"
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
  "outputs/figures/salary_by_education.png",
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
  "outputs/tables/salary_by_field.csv"
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
  "outputs/figures/salary_by_field.png",
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
  "outputs/tables/correlation_matrix.csv"
)
s

