suppressPackageStartupMessages({
  library(jsonlite)
  library(randomForest)
  library(caret)
  library(dplyr)
})

# Dynamically set working directory to project root (works on Windows, Linux, RStudio, Streamlit Cloud)
try({
  script_args <- commandArgs(trailingOnly = FALSE)
  file_arg <- grep("--file=", script_args, value = TRUE)
  if (length(file_arg) > 0) {
    script_path <- sub("--file=", "", file_arg[1])
    project_root <- normalizePath(file.path(dirname(script_path), ".."), winslash = "/")
    if (dir.exists(project_root)) setwd(project_root)
  } else if (!file.exists("models/employment_model_R.rds") && file.exists("../models/employment_model_R.rds")) {
    setwd("..")
  } else if (!file.exists("models/employment_model_R.rds")) {
    setwd("C:/Users/user/OneDrive - Sri Lanka Institute of Information Technology/OOP/Documents/SLIIT 3.1/IT3081 - Statistical Modeling/Graduate Employment Analysis")
  }
}, silent = TRUE)

# Read input JSON (or use sample student for manual interactive testing in RStudio)
args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  input_json_str <- '[{"age":26,"gender":"Female","country_of_origin":"India","visa_type":"Post-study","education_level":"Master\'s","field_of_study":"IT","university_ranking":"High","gpa":3.8,"internship_experience":"Yes","language_proficiency":"Fluent","region_of_study":"UK","years_since_graduation":2}]'
} else {
  input_json_str <- args[1]
}

input_data <- fromJSON(input_json_str)

# Load the trained R models safely
model_path <- "models/employment_model_R.rds"
salary_model_path <- "models/salary_model_R.rds"

if (!file.exists(model_path)) {
  stop("Employment model file not found. Please run train_model.R first.")
}

rf_model <- tryCatch({
  readRDS(model_path)
}, error = function(e) {
  stop(paste("Failed to read employment model:", e$message))
})

lm_salary <- if (file.exists(salary_model_path)) {
  tryCatch({
    readRDS(salary_model_path)
  }, error = function(e) {
    warning(paste("Could not load salary model:", e$message))
    NULL
  })
} else {
  NULL
}

# Ensure factor levels match the trained model
edu_levels <- c("Bachelor's", "Diploma", "Master's", "PhD")
if ("education_level" %in% names(input_data)) {
  input_data$education_level <- factor(input_data$education_level, levels = edu_levels)
}

xlev <- if (!is.null(rf_model$xlevels)) rf_model$xlevels else if (!is.null(rf_model$finalModel$xlevels)) rf_model$finalModel$xlevels else NULL

if (!is.null(xlev)) {
  for (col in names(input_data)) {
    if (col %in% names(xlev)) {
      input_data[[col]] <- factor(input_data[[col]], levels = xlev[[col]])
    }
  }
} else {
  data_path <- "data/preprocessed/dataset_predictive.csv"
  if (file.exists(data_path)) {
    data_skel <- read.csv(data_path, stringsAsFactors = TRUE, nrows = 1000)
    for (col in names(input_data)) {
      if (col %in% names(data_skel) && is.factor(data_skel[[col]]) && col != "education_level") {
        input_data[[col]] <- factor(input_data[[col]], levels = levels(data_skel[[col]]))
      }
    }
  }
}
combined <- input_data

# Predict employment probability
prob_preds <- predict(rf_model, combined, type = "prob")
emp_prob <- as.numeric(prob_preds[1, "Employed"])

# Predict salary safely (ONLY if candidate is classified as Employed)
# If probability < 0.50, candidate is Unemployed, so no employment salary applies
predicted_salary <- if (emp_prob >= 0.5 && !is.null(lm_salary)) {
  tryCatch({
    pred_val <- predict(lm_salary, combined)
    as.numeric(pred_val[1])
  }, error = function(e) {
    if (!is.null(lm_salary$finalModel)) {
      tryCatch({
        as.numeric(predict(lm_salary$finalModel, combined)[1])
      }, error = function(e2) {
        warning(paste("Could not predict salary:", e$message))
        NULL
      })
    } else {
      warning(paste("Could not predict salary:", e$message))
      NULL
    }
  })
} else {
  NULL
}

# Output JSON result so Python can read it
result <- list(
  employed_probability = emp_prob,
  predicted_salary = if (is.null(predicted_salary)) unbox(NA) else unbox(predicted_salary)
)
cat(toJSON(result, auto_unbox = TRUE, null = "null"))

