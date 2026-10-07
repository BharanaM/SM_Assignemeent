# Loading the relevant packages (install if necessary)
packages <- c("tidyverse", "janitor", "skimr", "rstatix", "car", "effectsize", "broom", "scales", "here")
new_packages <- packages[!(packages %in% installed.packages()[,"Package"])]
if(length(new_packages)) install.packages(new_packages)

library(here)
library(tidyverse)
library(janitor)
library(skimr)
library(rstatix)
library(car)
library(effectsize)
library(broom)
library(scales)

# Loading the data set
df <- read_csv(here("data", "raw", "dataset_predictive.csv"))

# Checking the dataset size
cat("Number of rows:", nrow(df), "\n")
cat("Number of columns:", ncol(df), "\n")

# Checking column names
names(df)

# Clean column names
df <- df %>% clean_names()

names(df)

# checking the structure 
str(df)
glimpse(df)

# Summary
summary(df)
skim(df)

# Missing Values
missing_counts <- colSums(is.na(df))
missing_percentage <- round(colMeans(is.na(df)) * 100, 2)

# Create missing_table to fix the export bug
missing_table <- data.frame(
  variable = names(missing_counts),
  missing_count = missing_counts,
  missing_percentage = missing_percentage,
  row.names = NULL
)
print(missing_table)

# Duplicates
duplicate_count <- sum(duplicated(df))
cat("Number of duplicate rows:", duplicate_count, "\n")

duplicates <- df %>% filter(duplicated(.))

# Unique values of every variable
for (column in names(df)) {
  cat("\n============================\n")
  cat("VARIABLE:", column, "\n")
  cat("============================\n")
  print(head(unique(df[[column]]), 20))
}

# Frequency of each categorical variable
for (column in names(df)) {
  if (is.character(df[[column]]) || is.factor(df[[column]])) {
    cat("\n============================\n")
    cat("VARIABLE:", column, "\n")
    cat("============================\n")
    print(df %>% count(.data[[column]]) %>% arrange(desc(n)))
  }
}

# Numerical variables
numeric_columns <- df %>% select(where(is.numeric)) %>% names()
print(numeric_columns)

# Export the first inspection results
dir.create(here("outputs", "tables"), recursive = TRUE, showWarnings = FALSE)
write_csv(missing_table, here("outputs", "tables", "missing_value_summary.csv"))
