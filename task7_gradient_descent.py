# TASK 7: CALCULUS AND OPTIMISATION
# What this program does:
#   1. Understand the cost function
#   2. Calculate the derivatives of the cost function
#   3. Implement gradient descent
#   4. Watch how the parameters change
#
# Idea: the model starts with wrong weights (all zero). In every
# step we check how wrong it is (cost), find which direction makes
# the cost smaller (derivative), and take a small step that way.

import os

# Always work inside the project folder, so the data folder is found
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("data/weather_clean.csv")
factors = ["Humidity", "Pressure_hPa", "Sunshine_Hours",
           "Rainfall_mm", "Previous_Day_Temp"]

# ------------------------------------------------------------
# STEP 1: Prepare the data
#   Put every factor on the same scale (standardisation):
#       new value = (value - mean) / standard deviation
#   Gradient descent works faster with scaled data.
# ------------------------------------------------------------
X = df[factors].to_numpy(dtype=float)
X = (X - X.mean(axis=0)) / X.std(axis=0)
y = df["Avg_Temperature"].to_numpy(dtype=float)
n = len(y)                                  # number of days

# ------------------------------------------------------------
# STEP 2: The formulas
#   prediction = X x w + b          (w = weights, b = intercept)
#   error      = prediction - actual
#
#   COST FUNCTION   : J = (1 / 2n) x sum of (error squared)
#   DERIVATIVES     : dJ/dw = (1 / n) x X-transpose x error
#                     dJ/db = (1 / n) x sum of error
#   UPDATE RULE     : w = w - learning_rate x dJ/dw
#                     b = b - learning_rate x dJ/db
# ------------------------------------------------------------

# ------------------------------------------------------------
# STEP 3: Gradient descent
# ------------------------------------------------------------
learning_rate = 0.1      # size of each step
epochs = 200             # number of steps

w = np.zeros(5)          # start with all weights = 0
b = 0                    # start with intercept = 0
cost_list = []

print("Epoch   Cost      Intercept(b)   w(Humidity)   w(Previous_Day_Temp)")

for epoch in range(epochs + 1):
    # make predictions and find the errors
    prediction = X @ w + b
    error = prediction - y

    # cost (how wrong the model is)
    cost = (error ** 2).sum() / (2 * n)
    cost_list.append(cost)

    # print the values at some epochs to see the change
    if epoch in [0, 1, 5, 10, 20, 50, 100, 200]:
        print(epoch, "    ", round(cost, 3), "    ", round(b, 3),
              "    ", round(w[0], 3), "    ", round(w[4], 3))

    # derivatives (slopes)
    dw = X.T @ error / n
    db = error.sum() / n

    # take a small step downhill
    w = w - learning_rate * dw
    b = b - learning_rate * db

print("\nCost came down from", round(cost_list[0], 2), "to", round(cost_list[-1], 3))

# ------------------------------------------------------------
# STEP 4: Check the answer with the matrix method (Task 6)
# ------------------------------------------------------------
X_new = np.hstack([np.ones((n, 1)), X])
exact = np.linalg.inv(X_new.T @ X_new) @ X_new.T @ y

print("\nGradient descent  [b, w...]:", np.round([b] + list(w), 3))
print("Exact answer      [b, w...]:", np.round(exact, 3))
print("Both are almost the same, so gradient descent works.")

# ------------------------------------------------------------
# STEP 5: Try three learning rates (50 steps each)
# ------------------------------------------------------------
print("\nCost after 50 steps with different learning rates:")
all_costs = {}
for rate in [0.01, 0.1, 0.5]:
    w2 = np.zeros(5)
    b2 = 0
    costs = []
    for step in range(51):
        error = X @ w2 + b2 - y
        costs.append((error ** 2).sum() / (2 * n))
        w2 = w2 - rate * (X.T @ error / n)
        b2 = b2 - rate * (error.sum() / n)
    all_costs[rate] = costs
    print("Learning rate", rate, "-> cost =", round(costs[-1], 4))

# ------------------------------------------------------------
# STEP 6: Draw the graphs
# ------------------------------------------------------------
plt.figure(figsize=(11, 4))

plt.subplot(1, 2, 1)
plt.plot(cost_list, color="teal")
plt.title("Cost decreases during gradient descent")
plt.xlabel("Epoch")
plt.ylabel("Cost")

plt.subplot(1, 2, 2)
for rate in all_costs:
    plt.plot(all_costs[rate], label="learning rate = " + str(rate))
plt.title("Effect of learning rate")
plt.xlabel("Epoch")
plt.ylabel("Cost")
plt.legend()

plt.tight_layout()
plt.show()          # show the graph on screen (close the window to continue)
