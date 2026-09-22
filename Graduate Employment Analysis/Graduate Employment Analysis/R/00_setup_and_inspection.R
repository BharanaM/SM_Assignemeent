# Installing the relevant packages a
install.packages(c(
  "tidyverse",
  "janitor",
  "skimr",
  "rstatix",
  "car",
  "effectsize",
  "broom",
  "scales"
))

# Loading the relevant packages
library(tidyverse)
library(janitor)
library(skimr)
library(rstatix)
library(car)
library(effectsize)
library(broom)
library(scales)

# Loading the data set
df <- read_csv("data/dataset.csv")

# Checking the dataset size
cat("Number of rows:", nrow(df), "\n")
cat("Number of columns:", ncol(df), "\n")

# Checking column names
names(df)

# Clean column names
df <- df %>%
  clean_names()

names(df)

# checking the structure 
str(df)

glimpse(df)

# Summary
summary(df)

skim(df)

# Missing Values
missing_counts <- colSums(is.na(df))
missing_counts

missing_percentage <- round(
  colMeans(is.na(df)) * 100,
  2
)
missing_percentage

# Duplicates
duplicate_count <- sum(duplicated(df))
cat(
  "Number of duplicate rows:",
  duplicate_count,
  "\n"
)

duplicates <- df %>%
  filter(duplicated(.))
duplicates


# Unique values of every variable
for (column in names(df)) {
  
  cat("\n============================\n")
  cat("VARIABLE:", column, "\n")
  cat("============================\n")
  
  print(head(unique(df[[column]]), 20))
}

# Frequency of each categorical variable
for (column in names(df)) {
  
  if (is.character(df[[column]]) ||
      is.factor(df[[column]])) {
    
    cat("\n============================\n")
    cat("VARIABLE:", column, "\n")
    cat("============================\n")
    
    print(
      df %>%
        count(.data[[column]]) %>%
        arrange(desc(n))
    )
  }
}

# Numerical variables
numeric_columns <- df %>%
  select(where(is.numeric)) %>%
  names()
numeric_columns

# Export the first inspection results
write_csv(
  missing_table,
  "Outputs/tables/missing_value_summary.csv"
)




