# TASK 4: CORRELATION ANALYSIS
# What this program does:
#   1. Pearson correlation
#   2. Spearman correlation
#   3. Correlation matrix
#   4. Find the strongest factors linked with temperature
#
# Correlation is a number between -1 and +1:
#   +1 = both go up together,  -1 = one goes up, the other goes down,
#    0 = no relationship

import os

# Always work inside the project folder, so the data folder is found
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)

df = pd.read_csv("data/weather_clean.csv")

factors = ["Humidity", "Rainfall_mm", "Wind_Speed", "Pressure_hPa",
           "Cloud_Cover", "Sunshine_Hours", "Previous_Day_Temp"]

# ------------------------------------------------------------
# STEP 1 and 2: Pearson and Spearman correlation with temperature
#   Pearson  = straight-line relationship
#   Spearman = relationship based on the rank (order) of values
# ------------------------------------------------------------
print("Correlation of each factor with Avg_Temperature")
print("Factor              Pearson   Spearman")

for factor in factors:
    pearson, p1 = stats.pearsonr(df[factor], df["Avg_Temperature"])
    spearman, p2 = stats.spearmanr(df[factor], df["Avg_Temperature"])
    print(factor.ljust(19), round(pearson, 3), "  ", round(spearman, 3))

# ------------------------------------------------------------
# STEP 3: Correlation matrix
# ------------------------------------------------------------
columns = factors + ["Avg_Temperature"]
matrix = df[columns].corr()

print("\nCorrelation matrix:")
print(matrix.round(2))

plt.figure(figsize=(9, 7))
plt.imshow(matrix, cmap="RdYlBu_r", vmin=-1, vmax=1)    # colour map: red = +1, blue = -1
plt.colorbar()
plt.xticks(range(len(columns)), columns, rotation=90)
plt.yticks(range(len(columns)), columns)

# write the correlation number inside every box
for row in range(len(columns)):
    for col in range(len(columns)):
        plt.text(col, row, round(matrix.iloc[row, col], 2),
                 ha="center", va="center", fontsize=8)
plt.title("Correlation Matrix of Weather Variables")
plt.tight_layout()
plt.show()          # show the graph on screen (close the window to continue)

# ------------------------------------------------------------
# STEP 4: Strongest factors
#   Ignore the + or - sign and sort from largest to smallest
# ------------------------------------------------------------
strength = matrix["Avg_Temperature"].drop("Avg_Temperature").abs()
strength = strength.sort_values(ascending=False)

print("\nFactors from strongest to weakest:")
for factor in strength.index:
    print(factor.ljust(19), round(strength[factor], 3))

print("\nStrongest factor:", strength.index[0])
