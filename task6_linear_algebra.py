# TASK 6: LINEAR ALGEBRA IMPLEMENTATION
# What this program does:
#   1. Represent weather data as vectors and matrices
#   2. Matrix addition and multiplication
#   3. Dot product
#   4. Show how matrices are used in regression

import os

# Always work inside the project folder, so the data folder is found
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np

df = pd.read_csv("data/weather_clean.csv")
factors = ["Humidity", "Pressure_hPa", "Sunshine_Hours",
           "Rainfall_mm", "Previous_Day_Temp"]

# ------------------------------------------------------------
# STEP 1: Vectors and matrices
# ------------------------------------------------------------
# A VECTOR is a list of numbers. One day of weather = one vector.
day1 = df.loc[0, factors].to_numpy(dtype=float)
print("Weather of day 1 (a vector):", day1)
print("Shape of the vector:", day1.shape)

# A MATRIX is a table of numbers. All days together = one matrix.
# Each row is one day, each column is one factor.
X = df[factors].to_numpy(dtype=float)
y = df["Avg_Temperature"].to_numpy(dtype=float)
print("\nMatrix X has shape:", X.shape, "(1000 days, 5 factors)")
print("First 3 days of X:")
print(X[:3])

# ------------------------------------------------------------
# STEP 2: Matrix addition and multiplication
# ------------------------------------------------------------
A = X[:3, :3]                  # a small 3 x 3 matrix
B = np.array([[2, 2, 2],
              [2, 2, 2],
              [2, 2, 2]])

print("\nMatrix A:")
print(A)
print("\nMatrix addition A + B (adds 2 to every number):")
print(A + B)
print("\nTranspose of A (rows become columns):")
print(A.T)
print("\nMatrix multiplication A x A-transpose:")
print((A @ A.T).round(1))

# ------------------------------------------------------------
# STEP 3: Dot product
#   Multiply the matching numbers, then add them all.
# ------------------------------------------------------------
weights = np.array([-0.1, 0.0, 0.2, 0.0, 0.9])

dot = np.dot(weights, day1)
print("\nDot product of weights and day 1 =", round(dot, 3))

# The same answer by hand:
by_hand = 0
for i in range(5):
    by_hand = by_hand + weights[i] * day1[i]
print("Same answer by hand              =", round(by_hand, 3))

# One matrix multiplication gives the answer for ALL days at once
all_days = X @ weights
print("Answers for the first 5 days:", all_days[:5].round(2))

# ------------------------------------------------------------
# STEP 4: Matrices in regression
#   Regression finds the best weights using this formula:
#       beta = (X^T X)^-1  X^T y
#   (the "Normal Equation")
# ------------------------------------------------------------
# Add a column of 1s so the model can also learn the intercept
ones = np.ones((len(X), 1))
X_new = np.hstack([ones, X])

XT_X = X_new.T @ X_new                 # X-transpose times X
XT_y = X_new.T @ y                     # X-transpose times y
beta = np.linalg.inv(XT_X) @ XT_y      # inverse of (X^T X) times (X^T y)

print("\nBest weights found with matrices:")
print("Intercept        :", round(beta[0], 4))
for i in range(5):
    print(factors[i].ljust(17), ":", round(beta[i + 1], 4))

# Use the weights to predict temperature
predicted = X_new @ beta
print("\nActual temperature   :", y[:5])
print("Predicted temperature:", predicted[:5].round(1))
