# TASK 2: DESCRIPTIVE AND INFERENTIAL STATISTICS
# What this program does:
#   1. Mean, median and mode
#   2. Variance and standard deviation
#   3. Analyse the temperature distribution
#   4. Sampling techniques
#   5. Hypothesis testing to compare two groups

import os

# Always work inside the project folder, so the data folder is found
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("data/weather_clean.csv")
temp = df["Avg_Temperature"]          # the column we are studying

# ------------------------------------------------------------
# STEP 1: Mean, median and mode
# ------------------------------------------------------------
print("----- Mean, Median, Mode -----")
print("Mean   :", round(temp.mean(), 2))
print("Median :", round(temp.median(), 2))
print("Mode   :", temp.mode()[0])

# ------------------------------------------------------------
# STEP 2: Variance and standard deviation
# ------------------------------------------------------------
print("\n----- Variance and Standard Deviation -----")
print("Variance           :", round(temp.var(), 2))
print("Standard deviation :", round(temp.std(), 2))
print("Minimum            :", temp.min())
print("Maximum            :", temp.max())

# ------------------------------------------------------------
# STEP 3: Distribution of temperature
# ------------------------------------------------------------
print("\n----- Distribution -----")
print("Skewness :", round(temp.skew(), 3), "(close to 0 means symmetric)")

print("\nAverage temperature of each city:")
print(df.groupby("City")["Avg_Temperature"].mean().round(2))

# Draw a histogram and a box plot
plt.figure(figsize=(11, 4))

plt.subplot(1, 2, 1)
plt.hist(temp, bins=25, color="teal", edgecolor="white")
plt.axvline(temp.mean(), color="orange", linewidth=2, label="mean")
plt.title("Distribution of Temperature")
plt.xlabel("Temperature (°C)")
plt.legend()

plt.subplot(1, 2, 2)
df.boxplot(column="Avg_Temperature", by="City", ax=plt.gca())
plt.title("Temperature by City")
plt.suptitle("")

plt.tight_layout()
plt.show()          # show the graph on screen (close the window to continue)

# ------------------------------------------------------------
# STEP 4: Sampling techniques
# ------------------------------------------------------------
print("\n----- Sampling (100 days each) -----")
print("Population mean:", round(temp.mean(), 2))

# (a) Simple random sampling: pick 100 days completely at random
simple = df.sample(n=100, random_state=1)
print("Simple random sample mean:", round(simple["Avg_Temperature"].mean(), 2))

# (b) Stratified sampling: pick 20 days from each of the 5 cities
stratified = df.groupby("City").sample(n=20, random_state=1)
print("Stratified sample mean   :", round(stratified["Avg_Temperature"].mean(), 2))

# (c) Systematic sampling: pick every 10th day
systematic = df.iloc[::10]
print("Systematic sample mean   :", round(systematic["Avg_Temperature"].mean(), 2))

# 95% confidence interval for the mean (from the simple random sample)
sample_temp = simple["Avg_Temperature"]
low, high = stats.t.interval(0.95, len(sample_temp) - 1,
                             loc=sample_temp.mean(),
                             scale=stats.sem(sample_temp))
print("95% confidence interval  :", round(low, 2), "to", round(high, 2))

# ------------------------------------------------------------
# STEP 5: Hypothesis testing
# ------------------------------------------------------------
# Test 1: Is the temperature different on rainy days and dry days?
#   H0 (null hypothesis)       : both groups have the same mean temperature
#   H1 (alternative hypothesis): the mean temperatures are different
print("\n----- Hypothesis Test 1: Rainy days vs Dry days -----")
rainy = df[df["Rain_Today"] == "Yes"]["Avg_Temperature"]
dry = df[df["Rain_Today"] == "No"]["Avg_Temperature"]
print("Rainy days mean:", round(rainy.mean(), 2))
print("Dry days mean  :", round(dry.mean(), 2))

t_value, p_value = stats.ttest_ind(rainy, dry, equal_var=False)
print("t value:", round(t_value, 3))
print("p value:", round(p_value, 4))

# Rule: if p value is less than 0.05, reject H0
if p_value < 0.05:
    print("Result: reject H0. Rainy and dry days have different temperatures.")
else:
    print("Result: cannot reject H0. No significant difference.")

# Test 2: Do the 5 cities have different temperatures? (ANOVA test)
print("\n----- Hypothesis Test 2: Difference between cities -----")
chennai = df[df["City"] == "Chennai"]["Avg_Temperature"]
delhi = df[df["City"] == "Delhi"]["Avg_Temperature"]
mumbai = df[df["City"] == "Mumbai"]["Avg_Temperature"]
bengaluru = df[df["City"] == "Bengaluru"]["Avg_Temperature"]
kolkata = df[df["City"] == "Kolkata"]["Avg_Temperature"]

f_value, p_value2 = stats.f_oneway(chennai, delhi, mumbai, bengaluru, kolkata)
print("F value:", round(f_value, 2))
print("p value:", round(p_value2, 4))

if p_value2 < 0.05:
    print("Result: reject H0. The cities have different temperatures.")
else:
    print("Result: cannot reject H0. No significant difference.")
