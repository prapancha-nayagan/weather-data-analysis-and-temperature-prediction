# TASK 3: PROBABILITY ANALYSIS
# What this program does:
#   1. Probability of a hot day (temperature above 30 °C)
#   2. Conditional probability: hot day given humidity below 60 %
#   3. Bayes' theorem on a weather example
#   4. Law of large numbers

import os

# Always work inside the project folder, so the data folder is found
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("data/weather_clean.csv")
total = len(df)

# ------------------------------------------------------------
# STEP 1: Simple probability
#   P(Hot) = number of hot days / total number of days
# ------------------------------------------------------------
hot = df["Avg_Temperature"] > 30
p_hot = hot.sum() / total

print("----- Probability of a hot day -----")
print("Hot days (above 30 °C):", hot.sum(), "out of", total)
print("P(Hot) =", round(p_hot, 4))

# ------------------------------------------------------------
# STEP 2: Conditional probability
#   P(Hot | Low humidity) = P(Hot and Low humidity) / P(Low humidity)
# ------------------------------------------------------------
low_humidity = df["Humidity"] < 60

p_low = low_humidity.sum() / total
p_hot_and_low = (hot & low_humidity).sum() / total
p_hot_given_low = p_hot_and_low / p_low

print("\n----- Conditional probability -----")
print("P(Low humidity)         =", round(p_low, 4))
print("P(Hot and Low humidity) =", round(p_hot_and_low, 4))
print("P(Hot | Low humidity)   =", round(p_hot_given_low, 4))
print("A hot day is", round(p_hot_given_low / p_hot, 1),
      "times more likely when humidity is low.")

# ------------------------------------------------------------
# STEP 3: Bayes' theorem
#   Question: the sky is very cloudy (cloud cover above 60 %).
#   What is the probability that it rains?
#
#   P(Rain | Cloudy) = P(Cloudy | Rain) x P(Rain) / P(Cloudy)
# ------------------------------------------------------------
rain = df["Rain_Today"] == "Yes"
cloudy = df["Cloud_Cover"] > 60

p_rain = rain.sum() / total
p_cloudy = cloudy.sum() / total
p_cloudy_given_rain = (rain & cloudy).sum() / rain.sum()

p_rain_given_cloudy = p_cloudy_given_rain * p_rain / p_cloudy

print("\n----- Bayes' theorem -----")
print("P(Rain)          =", round(p_rain, 4))
print("P(Cloudy)        =", round(p_cloudy, 4))
print("P(Cloudy | Rain) =", round(p_cloudy_given_rain, 4))
print("P(Rain | Cloudy) =", round(p_rain_given_cloudy, 4))
print("A cloudy sky increases the chance of rain from",
      round(p_rain * 100, 1), "% to", round(p_rain_given_cloudy * 100, 1), "%")

# ------------------------------------------------------------
# STEP 4: Law of large numbers
#   When we take more observations, the sample mean comes
#   closer to the true mean.
# ------------------------------------------------------------
true_mean = df["Avg_Temperature"].mean()

# Pick random days one by one (1000 times)
rng = np.random.default_rng(0)
sample = rng.choice(df["Avg_Temperature"], size=total, replace=True)

# Mean after 1 day, after 2 days, after 3 days, ...
running_mean = np.cumsum(sample) / np.arange(1, total + 1)

print("\n----- Law of large numbers -----")
print("True mean:", round(true_mean, 3))
for size in [10, 50, 100, 500, 1000]:
    sample_mean = running_mean[size - 1]
    error = abs(sample_mean - true_mean)
    print("After", size, "days: mean =", round(sample_mean, 3),
          ", error =", round(error, 3))

plt.figure(figsize=(8, 4))
plt.plot(running_mean, color="teal", label="sample mean")
plt.axhline(true_mean, color="orange", linestyle="--", label="true mean")
plt.title("Law of Large Numbers")
plt.xlabel("Number of days")
plt.ylabel("Mean temperature (°C)")
plt.legend()
plt.tight_layout()
plt.show()          # show the graph on screen (close the window to continue)
