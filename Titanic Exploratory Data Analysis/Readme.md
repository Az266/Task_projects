
# Titanic Survival Analysis

**Tech Stack:** Python | Pandas | Matplotlib | Seaborn

## Overview

An Exploratory Data Analysis (EDA) project exploring how passenger characteristics were associated with survival rates aboard the Titanic.

This project demonstrates data cleaning, data exploration, statistical analysis, and visualisation using Python.

**Dataset:** [Titanic - Kaggle](https://www.kaggle.com/competitions/titanic/data)

## Research Questions

1. How did survival rates differ across passenger classes?
2. How did survival rates differ between male and female passengers?
3. Which age group had the highest survival rate?
4. How did survival rates vary by embarkation port?
5. What was the average age of survivors, overall and by gender?
6. What correlations existed between survival, age, fare, and passenger class?

## Data Exploration & Cleaning

- Inspected data types, missing values, duplicates, and summary statistics.
- Filled missing `Age` values using the mean.
- Filled missing `Embarked` values using the mode.
- Dropped `Cabin` due to extensive missing values.
- Converted `Pclass`, `Sex`, and `Embarked` to categorical data types.

## Analysis & Visualisation

- Calculated survival percentages by gender, passenger class, age group, and embarkation port.
- Calculated the average age of survivors, including male and female survivors.
- Created four bar charts to compare survival rates.
- Generated a correlation heatmap for `Survived`, `Age`, `Fare`, and `Pclass`.

## Key Findings

Based on the standard Kaggle Titanic training dataset:

- **Gender:** Female passengers had a higher survival rate (74.2%) than male passengers (18.9%).
- **Passenger Class:** First-class passengers had the highest survival rate (63.0%), compared with third-class passengers (24.2%).
- **Age:** Survival rates were compared across children, adults, and seniors.
- **Embarkation:** Survival rates were compared across the three embarkation ports.

## How to Run

### 1. Install Dependencies

```bash
pip install pandas matplotlib seaborn
```

### 2. Download Dataset

Download `train.csv` from Kaggle.

The script expects the dataset at:

`../data/train.csv`

### 3. Run the Analysis

Run the Python script from the appropriate working directory to generate summary statistics and visualisations.


## Limitations

- Missing age values were replaced with the mean, which may affect age-related findings.
- The analysis identifies associations, not causation.
- Passenger characteristics were mainly analysed separately.