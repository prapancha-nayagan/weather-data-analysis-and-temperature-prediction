# TASK 5: REGRESSION ANALYSIS
# Model 1: Simple Linear Regression   (Humidity  ->  Temperature)
# Model 2: Multiple Linear Regression (5 factors  ->  Temperature)
# Then compare the two models.

import os

# Always work inside the project folder, so the data folder is found
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

df = pd.read_csv("data/weather_clean.csv")

# ------------------------------------------------------------
# STEP 1: Split the data
#   80 % of days are used to teach the model (train),
#   20 % of days are kept hidden to test the model.
# ------------------------------------------------------------
train, test = train_test_split(df, test_size=0.2, random_state=42)
print("Training days:", len(train), " Testing days:", len(test))

# ------------------------------------------------------------
# STEP 2: MODEL 1 - Simple Linear Regression
#   Equation: Temperature = intercept + slope x Humidity
# ------------------------------------------------------------
model1 = LinearRegression()
model1.fit(train[["Humidity"]], train["Avg_Temperature"])

print("\n----- Model 1: Simple Linear Regression -----")
print("Intercept:", round(model1.intercept_, 3))
print("Slope    :", round(model1.coef_[0], 3))
print("Meaning  : when humidity rises by 1 %, temperature changes by",
      round(model1.coef_[0], 3), "°C")

pred1 = model1.predict(test[["Humidity"]])

# ------------------------------------------------------------
# STEP 3: MODEL 2 - Multiple Linear Regression
#   Temperature = intercept + w1 x Humidity + w2 x Pressure + ...
# ------------------------------------------------------------
factors = ["Humidity", "Pressure_hPa", "Sunshine_Hours",
           "Rainfall_mm", "Previous_Day_Temp"]

model2 = LinearRegression()
model2.fit(train[factors], train["Avg_Temperature"])

print("\n----- Model 2: Multiple Linear Regression -----")
print("Intercept:", round(model2.intercept_, 3))
for i in range(len(factors)):
    print(factors[i].ljust(18), "weight =", round(model2.coef_[i], 4))

pred2 = model2.predict(test[factors])

# ------------------------------------------------------------
# STEP 4: Compare the two models on the test days
#   R2   : closer to 1 is better (how much variation is explained)
#   RMSE : closer to 0 is better (average error in °C)
# ------------------------------------------------------------
actual = test["Avg_Temperature"]

r2_model1 = r2_score(actual, pred1)
r2_model2 = r2_score(actual, pred2)
rmse_model1 = np.sqrt(mean_squared_error(actual, pred1))
rmse_model2 = np.sqrt(mean_squared_error(actual, pred2))

print("\n----- Comparison -----")
print("Model 1 (Humidity only): R2 =", round(r2_model1, 3),
      ", RMSE =", round(rmse_model1, 3), "°C")
print("Model 2 (5 factors)    : R2 =", round(r2_model2, 3),
      ", RMSE =", round(rmse_model2, 3), "°C")

if r2_model2 > r2_model1:
    print("Model 2 (Multiple Linear Regression) is better.")
else:
    print("Model 1 (Simple Linear Regression) is better.")

# ------------------------------------------------------------
# STEP 5: Draw the graphs
# ------------------------------------------------------------
plt.figure(figsize=(11, 4.5))

plt.subplot(1, 2, 1)
plt.scatter(test["Humidity"], actual, s=12, color="teal", label="actual")
# draw the regression line using its equation: intercept + slope x humidity
x_line = [test["Humidity"].min(), test["Humidity"].max()]
y_line = [model1.intercept_ + model1.coef_[0] * x_line[0],
          model1.intercept_ + model1.coef_[0] * x_line[1]]
plt.plot(x_line, y_line, color="orange", linewidth=2, label="regression line")
plt.title("Simple Regression (R2 = " + str(round(r2_model1, 2)) + ")")
plt.xlabel("Humidity (%)")
plt.ylabel("Temperature (°C)")
plt.legend()

plt.subplot(1, 2, 2)
plt.scatter(actual, pred2, s=12, color="teal")
plt.plot([15, 36], [15, 36], color="orange", linestyle="--", label="perfect prediction")
plt.title("Multiple Regression (R2 = " + str(round(r2_model2, 2)) + ")")
plt.xlabel("Actual temperature (°C)")
plt.ylabel("Predicted temperature (°C)")
plt.legend()

plt.tight_layout()
plt.show()          # show the graph on screen (close the window to continue)
