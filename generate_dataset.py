"""
Generate the raw dataset: India daily weather records (about 1,000 rows).

The data is synthetic but follows real climate patterns:
  * each city has its own average temperature and seasonal swing
  * monsoon months (Jun-Sep) bring rain, cloud, humidity and cooler days
  * humidity falls and sunshine rises as temperature rises
A few missing values, duplicate rows and sensor errors are added on purpose
so that Task 1 (data cleaning) has real work to do.
"""
import os

# Always work inside the project folder, so the data folders are found
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

# city: (yearly mean temp, seasonal swing, monsoon rain strength)
cities = {
    "Chennai":   (29.0, 3.5, 0.5),
    "Delhi":     (25.5, 10.0, 0.7),
    "Mumbai":    (28.0, 3.0, 1.0),
    "Bengaluru": (24.5, 3.0, 0.6),
    "Kolkata":   (27.0, 6.5, 0.9),
}

frames = []
for city, (base, swing, rain_k) in cities.items():
    dates = pd.date_range("2023-01-01", "2023-12-31")
    doy = dates.dayofyear.values
    # temperature peaks around day 140 (late May)
    season = np.cos(2 * np.pi * (doy - 140) / 365)
    monsoon = ((dates.month >= 6) & (dates.month <= 9)).astype(float)

    # day-to-day weather "noise" that carries over from one day to the next
    noise = np.zeros(len(dates))
    for i in range(1, len(dates)):
        noise[i] = 0.6 * noise[i - 1] + rng.normal(0, 1.1)

    temp = base + swing * season - 2.0 * monsoon * rain_k + noise
    cloud = np.clip(25 + 45 * monsoon * rain_k + rng.normal(0, 15, len(dates)) - 2.0 * noise, 0, 100)
    rain_prob = np.clip(0.05 + 0.55 * monsoon * rain_k + 0.004 * (cloud - 40), 0.01, 0.95)
    rainfall = np.where(rng.random(len(dates)) < rain_prob, rng.gamma(1.6, 9.0, len(dates)), 0.0)
    temp = temp - 0.04 * rainfall
    humidity = np.clip(62 - 1.7 * (temp - base) + 0.25 * cloud + 0.15 * rainfall
                       + 8 * monsoon + rng.normal(0, 6, len(dates)), 18, 99)
    pressure = 1010 - 0.25 * (temp - base) - 3.0 * monsoon + rng.normal(0, 1.8, len(dates))
    wind = np.clip(11 + 4 * monsoon + 0.04 * rainfall + rng.normal(0, 3.5, len(dates)), 1, 45)
    sunshine = np.clip(9.5 - 0.075 * cloud - 0.05 * rainfall + 0.08 * (temp - base) + rng.normal(0, 0.9, len(dates)), 0, 13)

    df = pd.DataFrame({
        "City": city, "Date": dates,
        "Humidity": humidity, "Rainfall_mm": rainfall, "Wind_Speed": wind,
        "Pressure_hPa": pressure, "Cloud_Cover": cloud, "Sunshine_Hours": sunshine,
        "Avg_Temperature": temp,
    })
    # yesterday's temperature (computed on the full year before sampling)
    df["Previous_Day_Temp"] = df["Avg_Temperature"].shift(1) + rng.normal(0, 0.3, len(df))
    df.loc[0, "Previous_Day_Temp"] = df.loc[0, "Avg_Temperature"]
    # keep 200 random days per city -> 5 x 200 = 1,000 records
    frames.append(df.sample(200, random_state=7).sort_values("Date"))

data = pd.concat(frames, ignore_index=True)
data["Rain_Today"] = np.where(data["Rainfall_mm"] > 2.5, "Yes", "No")
data.insert(0, "Record_ID", [f"W{i:04d}" for i in range(1, len(data) + 1)])
data["Date"] = data["Date"].dt.strftime("%Y-%m-%d")

# round to realistic precision
for c in ["Humidity", "Rainfall_mm", "Wind_Speed", "Cloud_Cover", "Sunshine_Hours",
          "Avg_Temperature", "Previous_Day_Temp"]:
    data[c] = data[c].round(1)
data["Pressure_hPa"] = data["Pressure_hPa"].round(1)

# ---- add real-world dirt for Task 1 ----
for col, n in [("Humidity", 18), ("Wind_Speed", 15), ("Sunshine_Hours", 14),
               ("Pressure_hPa", 12), ("Previous_Day_Temp", 10)]:
    data.loc[rng.choice(len(data), n, replace=False), col] = np.nan      # missing values
bad = rng.choice(len(data), 4, replace=False)
data.loc[bad, "Humidity"] = [105.0, 112.5, 130.0, 108.0]                  # impossible humidity
data = pd.concat([data, data.sample(15, random_state=3)], ignore_index=True)  # duplicate rows
data = data.sample(frac=1, random_state=11).reset_index(drop=True)        # shuffle

os.makedirs("data", exist_ok=True)
data.to_csv("data/weather_data.csv", index=False)
print("Saved data/weather_data.csv with", data.shape[0], "rows and", data.shape[1], "columns")
