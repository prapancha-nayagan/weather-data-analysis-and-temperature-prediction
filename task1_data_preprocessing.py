# TASK 1: DATA PREPROCESSING
# What this program does:
#   1. Collect and load the dataset
#   2. Handle missing values
#   3. Handle duplicate records
#   4. Clean the data
#   5. Identify numerical and categorical variables

import os

# Always work inside the project folder, so the data folder is found
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np

# ------------------------------------------------------------
# STEP 1: Load the dataset
# ------------------------------------------------------------
df = pd.read_csv("data/weather_data.csv")

print("Rows and columns:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

# ------------------------------------------------------------
# STEP 2: Check missing values
# ------------------------------------------------------------
print("\nMissing values in each column:")
print(df.isnull().sum())

# ------------------------------------------------------------
# STEP 3: Remove duplicate records
# ------------------------------------------------------------
print("\nNumber of duplicate rows:", df.duplicated().sum())
df = df.drop_duplicates()
print("Rows after removing duplicates:", len(df))

# ------------------------------------------------------------
# STEP 4: Clean the data
# ------------------------------------------------------------
# Humidity is a percentage, so it can never be more than 100.
# Such values are sensor mistakes, so we mark them as missing.
wrong = df["Humidity"] > 100
print("\nWrong humidity values (above 100):", wrong.sum())
df.loc[wrong, "Humidity"] = np.nan

# Fill every missing value with the median of its column.
# (The median is not affected by extreme values.)
columns_to_fill = ["Humidity", "Wind_Speed", "Pressure_hPa",
                   "Sunshine_Hours", "Previous_Day_Temp"]
for column in columns_to_fill:
    df[column] = df[column].fillna(df[column].median())

# Change the Date column from text to a real date
df["Date"] = pd.to_datetime(df["Date"])

print("Missing values left after cleaning:", df.isnull().sum().sum())

# ------------------------------------------------------------
# STEP 5: Numerical and categorical variables
# ------------------------------------------------------------
numerical = ["Humidity", "Rainfall_mm", "Wind_Speed", "Pressure_hPa",
             "Cloud_Cover", "Sunshine_Hours", "Previous_Day_Temp",
             "Avg_Temperature"]
categorical = ["City", "Rain_Today"]

print("\nNumerical variables  :", numerical)
print("Categorical variables:", categorical)
print("Other columns        : Record_ID (identifier), Date")

# ------------------------------------------------------------
# Save the clean data. The next tasks will use this file.
# ------------------------------------------------------------
df.to_csv("data/weather_clean.csv", index=False)
print("\nClean data saved in data/weather_clean.csv with", len(df), "rows")
