# TASK 8: MODEL EVALUATION AND RESIDUAL ANALYSIS
# What this program does:
#   1. Calculate MAE, MSE, RMSE and R2 for BOTH models
#      (Simple Linear Regression and Multiple Linear Regression)
#   2. Compare the two models in one table
#   3. Compare actual and predicted temperature
#   4. Plot the residuals
#   5. Find out if the models over-estimate or under-estimate
#
# Residual = Actual - Predicted
#   Positive residual -> the model UNDER-estimated the temperature
#   Negative residual -> the model OVER-estimated the temperature

import os

# Always work inside the project folder, so the data folder is found
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

df = pd.read_csv("data/weather_clean.csv")
factors = ["Humidity", "Pressure_hPa", "Sunshine_Hours",
           "Rainfall_mm", "Previous_Day_Temp"]

# ------------------------------------------------------------
# STEP 1: Train both models (same split as Task 5)
# ------------------------------------------------------------
train, test = train_test_split(df, test_size=0.2, random_state=42)

# Model 1: Simple Linear Regression (Humidity only)
simple_model = LinearRegression()
simple_model.fit(train[["Humidity"]], train["Avg_Temperature"])

# Model 2: Multiple Linear Regression (5 factors)
multiple_model = LinearRegression()
multiple_model.fit(train[factors], train["Avg_Temperature"])

# Predict the temperature of the test days with both models
actual = test["Avg_Temperature"].to_numpy()
pred_simple = simple_model.predict(test[["Humidity"]])
pred_multiple = multiple_model.predict(test[factors])

# ------------------------------------------------------------
# STEP 2: Evaluation metrics for both models
#   MAE  = average error, ignoring the + or - sign
#   MSE  = average of the squared errors
#   RMSE = square root of MSE (error in °C)
#   R2   = share of the temperature change explained by the model
# ------------------------------------------------------------
# Simple model
mae_simple = mean_absolute_error(actual, pred_simple)
mse_simple = mean_squared_error(actual, pred_simple)
rmse_simple = np.sqrt(mse_simple)
r2_simple = r2_score(actual, pred_simple)

# Multiple model
mae_multiple = mean_absolute_error(actual, pred_multiple)
mse_multiple = mean_squared_error(actual, pred_multiple)
rmse_multiple = np.sqrt(mse_multiple)
r2_multiple = r2_score(actual, pred_multiple)

# Put both results in one table
comparison = pd.DataFrame(
    [[mae_simple, mse_simple, rmse_simple, r2_simple],
     [mae_multiple, mse_multiple, rmse_multiple, r2_multiple]],
    index=["Simple (Humidity)", "Multiple (5 factors)"],
    columns=["MAE", "MSE", "RMSE", "R2"])

print("----- Comparison of Simple and Multiple Regression (test data) -----")
print(comparison.round(3))

print("\nRMSE improved from", round(rmse_simple, 2), "to", round(rmse_multiple, 2), "°C")
print("MAE improved from", round(mae_simple, 2), "to", round(mae_multiple, 2), "°C")
print("The multiple model explains", round(r2_multiple * 100, 1),
      "% of the temperature change, the simple model only",
      round(r2_simple * 100, 1), "%.")

# Training score vs testing score (checks that the model is not memorising)
r2_train = r2_score(train["Avg_Temperature"], multiple_model.predict(train[factors]))
print("\nMultiple model: R2 on training days =", round(r2_train, 3),
      ", R2 on test days =", round(r2_multiple, 3))

# ------------------------------------------------------------
# STEP 3: Compare actual and predicted temperature
# ------------------------------------------------------------
table = pd.DataFrame()
table["City"] = test["City"].to_numpy()
table["Actual"] = actual
table["Pred_Simple"] = pred_simple.round(1)
table["Pred_Multiple"] = pred_multiple.round(1)
table["Residual_Multiple"] = (actual - pred_multiple).round(2)

print("\n----- Actual vs Predicted (first 10 test days) -----")
print(table.head(10).to_string(index=False))

# ------------------------------------------------------------
# STEP 4: Residuals (actual - predicted) of both models
# ------------------------------------------------------------
residual_simple = actual - pred_simple
residual_multiple = actual - pred_multiple

plt.figure(figsize=(14, 7.5))

# Row 1 = simple model, Row 2 = multiple model
models = [("Simple model", pred_simple, residual_simple),
          ("Multiple model", pred_multiple, residual_multiple)]

for row in range(2):
    name = models[row][0]
    predicted = models[row][1]
    residual = models[row][2]

    # Graph 1: residuals should be scattered evenly around 0
    plt.subplot(2, 3, row * 3 + 1)
    plt.scatter(predicted, residual, s=12, color="teal", alpha=0.6)
    plt.axhline(0, color="orange", linestyle="--")
    plt.title(name + ": residuals vs predicted")
    plt.xlabel("Predicted temperature (°C)")
    plt.ylabel("Residual")

    # Graph 2: residuals should look like a bell shape centred at 0
    plt.subplot(2, 3, row * 3 + 2)
    plt.hist(residual, bins=20, color="teal", edgecolor="white")
    plt.axvline(0, color="orange", linestyle="--")
    plt.title(name + ": residual distribution")
    plt.xlabel("Residual (°C)")

    # Graph 3: Q-Q plot, points on the line mean residuals are normal
    plt.subplot(2, 3, row * 3 + 3)
    stats.probplot(residual, plot=plt)
    plt.title(name + ": Q-Q plot")

plt.tight_layout()
plt.show()          # show the graph on screen (close the window to continue)

# ------------------------------------------------------------
# STEP 5: Over-estimating or under-estimating?
#   Residual below 0 -> over-estimated
#   Residual above 0 -> under-estimated
# ------------------------------------------------------------
print("\n----- Over-estimate or Under-estimate? -----")

over_simple = (residual_simple < 0).sum()
under_simple = (residual_simple > 0).sum()
print("Simple model  : mean residual =", round(residual_simple.mean(), 3),
      "| over-estimated", over_simple, "days | under-estimated", under_simple, "days")
print("                largest over-estimate  =", round(residual_simple.min(), 1), "°C,",
      "largest under-estimate =", round(residual_simple.max(), 1), "°C")

over_multiple = (residual_multiple < 0).sum()
under_multiple = (residual_multiple > 0).sum()
print("Multiple model: mean residual =", round(residual_multiple.mean(), 3),
      "| over-estimated", over_multiple, "days | under-estimated", under_multiple, "days")
print("                largest over-estimate  =", round(residual_multiple.min(), 1), "°C,",
      "largest under-estimate =", round(residual_multiple.max(), 1), "°C")

if abs(residual_multiple.mean()) < 0.1:
    print("\nConclusion: the multiple model is balanced. It does not")
    print("over-estimate or under-estimate the temperature overall.")
elif residual_multiple.mean() < 0:
    print("\nConclusion: the multiple model over-estimates the temperature.")
else:
    print("\nConclusion: the multiple model under-estimates the temperature.")

# Does the multiple model make bigger mistakes for cold or hot days?
bands = pd.cut(actual, [0, 20, 30, 50], labels=["below 20", "20 to 30", "above 30"])
band_table = pd.DataFrame({"Band": bands, "Residual": residual_multiple})
band_table = band_table.groupby("Band", observed=True)["Residual"].agg(["count", "mean"]).round(2)
band_table.columns = ["Days", "Mean residual"]
print("\nMean residual of the multiple model for each temperature band:")
print(band_table)

# Are the residuals normally distributed? (Shapiro-Wilk test)
w_value, p_value = stats.shapiro(residual_multiple)
print("\nShapiro-Wilk test on residuals: p value =", round(p_value, 3))
if p_value > 0.05:
    print("Residuals look normally distributed (good).")
else:
    print("Residuals are not perfectly normal, but the model is still useful.")
