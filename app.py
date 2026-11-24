# WEATHER DATA ANALYSIS AND TEMPERATURE PREDICTION - WEBSITE
#
# Run it with:   streamlit run app.py
# It opens at:   http://localhost:8501
#
# The website has 12 pages. Choose a page from the menu on the left.
# Every page is written step by step, so it is easy to read:
#   if page == "...":
#       (code of that page)

import os
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Always work inside the project folder, so the data folder is found
os.chdir(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Weather Data Analysis", page_icon="🌤️", layout="wide")

# ------------------------------------------------------------
# SETTINGS USED BY MANY PAGES
# ------------------------------------------------------------
FACTORS = ["Humidity", "Pressure_hPa", "Sunshine_Hours", "Rainfall_mm", "Previous_Day_Temp"]
ALL_VARIABLES = ["Avg_Temperature", "Humidity", "Rainfall_mm", "Pressure_hPa",
                 "Wind_Speed", "Sunshine_Hours", "Cloud_Cover", "Previous_Day_Temp"]
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# position of each city on the map
CITY_POSITION = {
    "Chennai": (13.08, 80.27), "Delhi": (28.61, 77.21), "Mumbai": (19.08, 72.88),
    "Bengaluru": (12.97, 77.59), "Kolkata": (22.57, 88.36),
}

# ------------------------------------------------------------
# LOAD THE DATA (made by Task 1)
# ------------------------------------------------------------
if not os.path.exists("data/weather_clean.csv"):
    st.error("The file data/weather_clean.csv was not found. "
             "Please run task1_data_preprocessing.py first.")
    st.stop()


@st.cache_data
def load_data():
    data = pd.read_csv("data/weather_clean.csv")
    data["Date"] = pd.to_datetime(data["Date"])
    data["Month"] = data["Date"].dt.month
    return data


df = load_data()
cities = sorted(df["City"].unique())

# ------------------------------------------------------------
# TRAIN THE TWO MODELS (same split and models as Task 5 and Task 8)
# ------------------------------------------------------------
train, test = train_test_split(df, test_size=0.2, random_state=42)

simple_model = LinearRegression().fit(train[["Humidity"]], train["Avg_Temperature"])
multiple_model = LinearRegression().fit(train[FACTORS], train["Avg_Temperature"])

actual = test["Avg_Temperature"].to_numpy()
pred_simple = simple_model.predict(test[["Humidity"]])
pred_multiple = multiple_model.predict(test[FACTORS])

rmse_multiple = np.sqrt(mean_squared_error(actual, pred_multiple))
r2_multiple = r2_score(actual, pred_multiple)

# ------------------------------------------------------------
# SIDEBAR MENU
# ------------------------------------------------------------
PAGES = [
    "🏠 Project Info",
    "📋 Dataset",
    "📈 Trends",
    "⚖️ City Comparison",
    "🔮 Predict Temperature",
    "🎲 Probability Calculator",
    "🔗 Correlation",
    "🧪 Hypothesis Test",
    "⛰️ Gradient Descent",
    "📏 Model Performance",
    "🗺️ Map",
    "📤 Upload Your Data",
]

st.sidebar.title("🌤️ Weather Analysis")
page = st.sidebar.radio("Go to page", PAGES)
st.sidebar.divider()
st.sidebar.caption(str(len(df)) + " daily records | " + str(len(cities)) + " cities")
st.sidebar.caption("Model R² on test days: " + str(round(r2_multiple, 3)))


# ============================================================
# PAGE 1: PROJECT INFO
# ============================================================
if page == "🏠 Project Info":
    st.title("🌤️ Weather Data Analysis and Temperature Prediction")
    st.write("This website shows the whole project: the dataset, the statistics, "
             "the models, and a tool that predicts the temperature.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Records", len(df))
    col2.metric("Cities", len(cities))
    col3.metric("Average temperature", str(round(df["Avg_Temperature"].mean(), 1)) + " °C")
    col4.metric("Model accuracy (R²)", round(r2_multiple, 3))

    st.subheader("The 8 tasks of the project")
    tasks = pd.DataFrame({
        "Task": ["1. Data preprocessing", "2. Descriptive and inferential statistics",
                 "3. Probability analysis", "4. Correlation analysis",
                 "5. Regression analysis", "6. Linear algebra",
                 "7. Calculus and optimisation", "8. Model evaluation"],
        "What it does": ["Load data, remove duplicates, fill missing values",
                         "Mean, spread, sampling, hypothesis tests",
                         "Probability, conditional probability, Bayes, law of large numbers",
                         "Pearson and Spearman correlation, correlation matrix",
                         "Simple and multiple linear regression",
                         "Vectors, matrices, dot product, normal equation",
                         "Cost function, derivatives, gradient descent",
                         "MAE, MSE, RMSE, R², residual analysis"],
        "Page in this website": ["📋 Dataset", "⚖️ City Comparison, 🧪 Hypothesis Test",
                                 "🎲 Probability Calculator", "🔗 Correlation",
                                 "🔮 Predict Temperature", "🔮 Predict Temperature",
                                 "⛰️ Gradient Descent", "📏 Model Performance"],
    })
    st.table(tasks.set_index("Task"))

    st.subheader("Dark and light theme")
    st.write("Click the ⋮ menu at the top right, then **Settings**, then choose **Theme** "
             "(Light, Dark, or Use system setting).")


# ============================================================
# PAGE 2: DATASET (filters, summary cards, download)
# ============================================================
if page == "📋 Dataset":
    st.title("📋 Dataset")

    # --- filters ---
    col1, col2, col3 = st.columns(3)
    chosen_cities = col1.multiselect("Cities", cities, default=cities)
    month_from, month_to = col2.select_slider("Months", options=MONTH_NAMES,
                                              value=("Jan", "Dec"))
    rain_choice = col3.radio("Rain today", ["All", "Yes", "No"], horizontal=True)

    first_month = MONTH_NAMES.index(month_from) + 1
    last_month = MONTH_NAMES.index(month_to) + 1

    filtered = df[df["City"].isin(chosen_cities)]
    filtered = filtered[(filtered["Month"] >= first_month) & (filtered["Month"] <= last_month)]
    if rain_choice != "All":
        filtered = filtered[filtered["Rain_Today"] == rain_choice]

    if len(filtered) == 0:
        st.warning("No records match these filters.")
    else:
        # --- summary cards ---
        temp = filtered["Avg_Temperature"]
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Records", len(filtered))
        col2.metric("Average temperature", str(round(temp.mean(), 1)) + " °C")
        col3.metric("Highest", str(round(temp.max(), 1)) + " °C")
        col4.metric("Lowest", str(round(temp.min(), 1)) + " °C")
        col5.metric("Hot days (above 30 °C)", int((temp > 30).sum()))

        # --- table and download button ---
        st.dataframe(filtered.drop(columns=["Month"]), width="stretch", hide_index=True)
        st.download_button("⬇️ Download this data (CSV)", filtered.to_csv(index=False),
                           file_name="filtered_weather_data.csv", mime="text/csv")

        st.subheader("Statistics of the selected records")
        st.dataframe(filtered[ALL_VARIABLES].describe().round(2), width="stretch")


# ============================================================
# PAGE 3: TRENDS
# ============================================================
if page == "📈 Trends":
    st.title("📈 How the weather changes through the year")

    col1, col2, col3 = st.columns(3)
    chosen_cities = col1.multiselect("Cities", cities, default=cities)
    variable = col2.selectbox("Weather variable", ALL_VARIABLES)
    view = col3.radio("View", ["Monthly average", "Daily points"], horizontal=True)

    if len(chosen_cities) == 0:
        st.warning("Please choose at least one city.")
    else:
        fig, ax = plt.subplots(figsize=(11, 4.5))
        monthly_all = pd.DataFrame()

        for city in chosen_cities:
            city_data = df[df["City"] == city]
            monthly = city_data.groupby("Month")[variable].mean()
            monthly_all[city] = monthly

            if view == "Monthly average":
                ax.plot(monthly.index, monthly.values, marker="o", label=city)
            else:
                ax.scatter(city_data["Date"], city_data[variable], s=10, alpha=0.6, label=city)

        if view == "Monthly average":
            ax.set_xticks(range(1, 13))
            ax.set_xticklabels(MONTH_NAMES)
        ax.set_ylabel(variable)
        ax.set_title(variable + " through the year")
        ax.grid(alpha=0.3)
        ax.legend()
        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Monthly averages")
        monthly_all.index = [MONTH_NAMES[m - 1] for m in monthly_all.index]
        st.dataframe(monthly_all.round(2), width="stretch")
        st.download_button("⬇️ Download monthly averages (CSV)", monthly_all.round(2).to_csv(),
                           file_name="monthly_averages.csv", mime="text/csv")


# ============================================================
# PAGE 4: CITY COMPARISON
# ============================================================
if page == "⚖️ City Comparison":
    st.title("⚖️ Compare two cities")

    col1, col2 = st.columns(2)
    city_a = col1.selectbox("First city", cities, index=0)
    city_b = col2.selectbox("Second city", cities, index=1)

    data_a = df[df["City"] == city_a]
    data_b = df[df["City"] == city_b]

    # --- summary cards for each city ---
    for column, name, data in [(col1, city_a, data_a), (col2, city_b, data_b)]:
        with column:
            st.subheader(name)
            c1, c2, c3 = st.columns(3)
            c1.metric("Average", str(round(data["Avg_Temperature"].mean(), 1)) + " °C")
            c2.metric("Highest", str(round(data["Avg_Temperature"].max(), 1)) + " °C")
            c3.metric("Lowest", str(round(data["Avg_Temperature"].min(), 1)) + " °C")
            c4, c5, c6 = st.columns(3)
            c4.metric("Spread (std)", str(round(data["Avg_Temperature"].std(), 1)) + " °C")
            c5.metric("Humidity", str(round(data["Humidity"].mean(), 1)) + " %")
            c6.metric("Rainy days", str(round((data["Rain_Today"] == "Yes").mean() * 100)) + " %")

    # --- charts side by side ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    for city, data in [(city_a, data_a), (city_b, data_b)]:
        monthly = data.groupby("Month")["Avg_Temperature"].mean()
        ax1.plot(monthly.index, monthly.values, marker="o", label=city)
    ax1.set_xticks(range(1, 13))
    ax1.set_xticklabels(MONTH_NAMES, fontsize=8)
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_title("Monthly average temperature")
    ax1.grid(alpha=0.3)
    ax1.legend()

    ax2.boxplot([data_a["Avg_Temperature"], data_b["Avg_Temperature"]])
    ax2.set_xticklabels([city_a, city_b])
    ax2.set_title("Temperature spread")
    ax2.set_ylabel("Temperature (°C)")
    ax2.grid(alpha=0.3)

    st.pyplot(fig)
    plt.close(fig)

    # --- is the difference real? (t-test) ---
    st.subheader("Is the difference real?")
    if city_a == city_b:
        st.info("Please choose two different cities.")
    else:
        t_value, p_value = stats.ttest_ind(data_a["Avg_Temperature"],
                                           data_b["Avg_Temperature"], equal_var=False)
        st.write("t value = **" + str(round(t_value, 3)) + "**, p value = **"
                 + str(round(p_value, 4)) + "**")
        if p_value < 0.05:
            st.success("The p value is below 0.05, so the average temperatures of "
                       + city_a + " and " + city_b + " are really different.")
        else:
            st.info("The p value is above 0.05, so there is no proof that the average "
                    "temperatures of the two cities are different.")


# ============================================================
# PAGE 5: PREDICT TEMPERATURE (with range, explanation, what-if)
# ============================================================
if page == "🔮 Predict Temperature":
    st.title("🔮 Predict the temperature")
    st.write("Move the sliders to describe a day. The model (Multiple Linear Regression "
             "from Task 5) predicts the average temperature.")

    # --- sliders for the 5 inputs ---
    values = []
    left, right = st.columns(2)
    for i in range(len(FACTORS)):
        name = FACTORS[i]
        low = float(df[name].min())
        high = float(df[name].max())
        average = float(df[name].mean())
        column = left if i % 2 == 0 else right
        values.append(column.slider(name, low, high, round(average, 1)))

    # --- the prediction ---
    new_day = pd.DataFrame([values], columns=FACTORS)
    prediction = multiple_model.predict(new_day)[0]

    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Predicted temperature", str(round(prediction, 1)) + " °C")
    col2.metric("Likely range (± RMSE)",
                str(round(prediction - rmse_multiple, 1)) + " to "
                + str(round(prediction + rmse_multiple, 1)) + " °C")
    col3.metric("Typical error (RMSE)", str(round(rmse_multiple, 2)) + " °C")
    st.caption("The real temperature is usually inside the range. The width of the range "
               "is the average error of the model on test days.")

    # --- why this prediction? (contribution of each input) ---
    st.subheader("Why this prediction?")
    average_day = pd.DataFrame([train[FACTORS].mean()], columns=FACTORS)
    base_temperature = multiple_model.predict(average_day)[0]
    contribution = multiple_model.coef_ * (np.array(values) - train[FACTORS].mean().to_numpy())

    fig, ax = plt.subplots(figsize=(8, 3))
    colors = ["#F26B21" if c > 0 else "#139A92" for c in contribution]
    ax.barh(FACTORS, contribution, color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Change in temperature (°C) compared with an average day")
    limit = max(1.0, np.abs(contribution).max() * 1.2)     # keep the scale fair for small changes
    ax.set_xlim(-limit, limit)
    ax.invert_yaxis()
    st.pyplot(fig)
    plt.close(fig)
    st.write("An average day gives **" + str(round(base_temperature, 1)) + " °C**. "
             "Orange bars push the temperature up, teal bars push it down.")

    # --- which factors matter most overall? ---
    st.subheader("Which factors matter most overall?")
    importance = np.abs(multiple_model.coef_ * train[FACTORS].std().to_numpy())
    importance = pd.Series(importance, index=FACTORS).sort_values(ascending=False)
    st.bar_chart(importance)
    st.caption("Importance = size of the weight x how much the factor varies.")

    # --- what-if curve ---
    st.subheader("What if one factor changes?")
    what_if = st.selectbox("Change this factor", FACTORS)
    low = float(df[what_if].min())
    high = float(df[what_if].max())
    steps = np.linspace(low, high, 50)

    curve = pd.DataFrame([values] * 50, columns=FACTORS)
    curve[what_if] = steps
    curve_prediction = multiple_model.predict(curve)

    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(steps, curve_prediction, color="#139A92", linewidth=2)
    ax.scatter([values[FACTORS.index(what_if)]], [prediction], color="#F26B21", s=80, zorder=3,
               label="your day")
    ax.set_xlabel(what_if)
    ax.set_ylabel("Predicted temperature (°C)")
    ax.grid(alpha=0.3)
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)
    st.caption("All other sliders stay as they are above.")


# ============================================================
# PAGE 6: PROBABILITY CALCULATOR (Task 3)
# ============================================================
if page == "🎲 Probability Calculator":
    st.title("🎲 Probability calculator")

    place = st.selectbox("Use data of", ["All cities"] + cities)
    if place == "All cities":
        data = df
    else:
        data = df[df["City"] == place]
    total = len(data)

    # --- 1. simple probability ---
    st.subheader("1. Probability of a hot day")
    limit = st.slider("Temperature limit (°C)", 10.0, 40.0, 30.0, 0.5)
    hot = data["Avg_Temperature"] > limit
    p_hot = hot.sum() / total
    col1, col2 = st.columns(2)
    col1.metric("P(Temperature > " + str(limit) + " °C)", round(p_hot, 4))
    col2.metric("Hot days", str(int(hot.sum())) + " of " + str(total))

    # --- 2. conditional probability ---
    st.subheader("2. Conditional probability")
    humidity_limit = st.slider("Humidity limit (%)", 20, 100, 60)
    low_humidity = data["Humidity"] < humidity_limit
    p_low = low_humidity.sum() / total
    p_both = (hot & low_humidity).sum() / total

    if p_low == 0:
        st.warning("No day has humidity below " + str(humidity_limit) + " %. Choose a higher limit.")
    else:
        p_hot_given_low = p_both / p_low
        col1, col2, col3 = st.columns(3)
        col1.metric("P(Low humidity)", round(p_low, 4))
        col2.metric("P(Hot and Low humidity)", round(p_both, 4))
        col3.metric("P(Hot | Low humidity)", round(p_hot_given_low, 4))
        st.write("Formula: P(Hot | Low humidity) = P(Hot and Low humidity) / P(Low humidity)")
        if p_hot > 0:
            st.info("A hot day is **" + str(round(p_hot_given_low / p_hot, 2))
                    + " times** as likely when humidity is below " + str(humidity_limit) + " %.")

    # --- 3. Bayes' theorem ---
    st.subheader("3. Bayes' theorem: is rain coming?")
    cloud_limit = st.slider("Cloudy sky means cloud cover above (%)", 10, 95, 60)
    rain = data["Rain_Today"] == "Yes"
    cloudy = data["Cloud_Cover"] > cloud_limit

    p_rain = rain.sum() / total
    p_cloudy = cloudy.sum() / total

    if rain.sum() == 0 or cloudy.sum() == 0:
        st.warning("Not enough rainy or cloudy days for this choice.")
    else:
        p_cloudy_given_rain = (rain & cloudy).sum() / rain.sum()
        p_rain_given_cloudy = p_cloudy_given_rain * p_rain / p_cloudy
        direct = (rain & cloudy).sum() / cloudy.sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("P(Rain)", round(p_rain, 4))
        col2.metric("P(Cloudy)", round(p_cloudy, 4))
        col3.metric("P(Cloudy | Rain)", round(p_cloudy_given_rain, 4))
        col4.metric("P(Rain | Cloudy)", round(p_rain_given_cloudy, 4))
        st.write("Formula: P(Rain | Cloudy) = P(Cloudy | Rain) x P(Rain) / P(Cloudy)")
        st.info("A cloudy sky changes the chance of rain from **" + str(round(p_rain * 100, 1))
                + " %** to **" + str(round(p_rain_given_cloudy * 100, 1)) + " %**. "
                "Direct count check: " + str(round(direct, 4)) + " (same answer).")


# ============================================================
# PAGE 7: CORRELATION (Task 4)
# ============================================================
if page == "🔗 Correlation":
    st.title("🔗 Correlation analysis")
    st.write("Correlation is a number between -1 and +1. +1 means both go up together, "
             "-1 means one goes up while the other goes down, 0 means no relationship.")

    method = st.radio("Method", ["pearson", "spearman"], horizontal=True)
    matrix = df[ALL_VARIABLES].corr(method=method)

    # --- heat map ---
    fig, ax = plt.subplots(figsize=(9, 7))
    picture = ax.imshow(matrix, cmap="RdYlBu_r", vmin=-1, vmax=1)
    plt.colorbar(picture)
    ax.set_xticks(range(len(ALL_VARIABLES)))
    ax.set_xticklabels(ALL_VARIABLES, rotation=90)
    ax.set_yticks(range(len(ALL_VARIABLES)))
    ax.set_yticklabels(ALL_VARIABLES)
    for row in range(len(ALL_VARIABLES)):
        for col in range(len(ALL_VARIABLES)):
            ax.text(col, row, round(matrix.iloc[row, col], 2), ha="center", va="center", fontsize=8)
    ax.set_title(method.capitalize() + " correlation matrix")
    st.pyplot(fig)
    plt.close(fig)

    # --- ranking ---
    st.subheader("Factors linked with temperature")
    ranking = matrix["Avg_Temperature"].drop("Avg_Temperature")
    ranking = ranking.reindex(ranking.abs().sort_values(ascending=False).index)
    ranking_table = pd.DataFrame({"Correlation": ranking.round(3),
                                  "Strength": ranking.abs().round(3)})
    st.dataframe(ranking_table, width="stretch")
    st.success("Strongest factor: **" + ranking.index[0] + "** (" + str(round(ranking.iloc[0], 3)) + ")")

    # --- scatter plot of one factor ---
    st.subheader("Look at one factor")
    factor = st.selectbox("Factor", list(ranking.index))
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.scatter(df[factor], df["Avg_Temperature"], s=10, alpha=0.5, color="#139A92")
    ax.set_xlabel(factor)
    ax.set_ylabel("Avg_Temperature (°C)")
    ax.grid(alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


# ============================================================
# PAGE 8: HYPOTHESIS TEST (Task 2)
# ============================================================
if page == "🧪 Hypothesis Test":
    st.title("🧪 Hypothesis test")
    st.write("A hypothesis test checks if a difference between groups is real or just luck.")

    test_type = st.radio("Choose a test", ["Rainy days vs dry days",
                                           "Two cities",
                                           "All 5 cities (ANOVA)"])
    alpha = st.select_slider("Significance level (alpha)", options=[0.01, 0.05, 0.10], value=0.05)

    if test_type == "Rainy days vs dry days":
        group_a = df[df["Rain_Today"] == "Yes"]["Avg_Temperature"]
        group_b = df[df["Rain_Today"] == "No"]["Avg_Temperature"]
        name_a, name_b = "Rainy days", "Dry days"
        st.write("**H0:** rainy and dry days have the same average temperature.")
        st.write("**H1:** the average temperatures are different.")

    if test_type == "Two cities":
        col1, col2 = st.columns(2)
        city_a = col1.selectbox("First city", cities, index=0)
        city_b = col2.selectbox("Second city", cities, index=1)
        group_a = df[df["City"] == city_a]["Avg_Temperature"]
        group_b = df[df["City"] == city_b]["Avg_Temperature"]
        name_a, name_b = city_a, city_b
        st.write("**H0:** " + city_a + " and " + city_b + " have the same average temperature.")
        st.write("**H1:** the average temperatures are different.")

    if test_type == "All 5 cities (ANOVA)":
        st.write("**H0:** all 5 cities have the same average temperature.")
        st.write("**H1:** at least one city is different.")
        groups = [df[df["City"] == city]["Avg_Temperature"] for city in cities]
        f_value, p_value = stats.f_oneway(*groups)

        means = df.groupby("City")["Avg_Temperature"].mean().round(2)
        st.dataframe(means.to_frame("Average temperature (°C)"), width="stretch")
        st.write("F value = **" + str(round(f_value, 2)) + "**, p value = **" + str(round(p_value, 5)) + "**")
        if p_value < alpha:
            st.success("p value is below " + str(alpha) + ": **reject H0**. The cities have different temperatures.")
        else:
            st.info("p value is not below " + str(alpha) + ": **cannot reject H0**. No proof of a difference.")

    else:
        col1, col2 = st.columns(2)
        col1.metric(name_a + " (average)", str(round(group_a.mean(), 2)) + " °C", str(len(group_a)) + " days")
        col2.metric(name_b + " (average)", str(round(group_b.mean(), 2)) + " °C", str(len(group_b)) + " days")

        if name_a == name_b:
            st.info("Please choose two different cities.")
        else:
            t_value, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)
            st.write("t value = **" + str(round(t_value, 3)) + "**, p value = **" + str(round(p_value, 4)) + "**")
            if p_value < alpha:
                st.success("p value is below " + str(alpha) + ": **reject H0**. The two groups really have different average temperatures.")
            else:
                st.info("p value is not below " + str(alpha) + ": **cannot reject H0**. There is no proof of a difference.")

            fig, ax = plt.subplots(figsize=(7, 3.5))
            ax.boxplot([group_a, group_b])
            ax.set_xticklabels([name_a, name_b])
            ax.set_ylabel("Temperature (°C)")
            ax.grid(alpha=0.3)
            st.pyplot(fig)
            plt.close(fig)


# ============================================================
# PAGE 9: GRADIENT DESCENT (Task 7)
# ============================================================
if page == "⛰️ Gradient Descent":
    st.title("⛰️ Gradient descent")
    st.write("The model starts with wrong weights (all zero). In every step it finds the "
             "direction that lowers the error (cost) and takes a small step that way.")
    st.latex(r"J = \frac{1}{2n}\sum(\hat{y}-y)^2 \qquad w = w - \alpha \frac{\partial J}{\partial w}")

    learning_rate = st.select_slider("Learning rate (step size)", options=[0.001, 0.01, 0.05, 0.1, 0.5], value=0.1)

    # --- prepare standardised data ---
    X = df[FACTORS].to_numpy(dtype=float)
    X = (X - X.mean(axis=0)) / X.std(axis=0)
    y = df["Avg_Temperature"].to_numpy(dtype=float)
    n = len(y)

    # --- run gradient descent for 300 epochs and remember every step ---
    epochs = 300
    w = np.zeros(5)
    b = 0.0
    cost_list = []
    w_list = []
    b_list = []

    for epoch in range(epochs + 1):
        error = X @ w + b - y
        cost_list.append((error ** 2).sum() / (2 * n))
        w_list.append(w.copy())
        b_list.append(b)
        w = w - learning_rate * (X.T @ error / n)
        b = b - learning_rate * (error.sum() / n)

    cost_list = np.array(cost_list)

    # --- show the result at the chosen epoch ---
    chosen = st.slider("Epoch (step number)", 0, epochs, 50)
    col1, col2, col3 = st.columns(3)
    col1.metric("Cost at this epoch", round(cost_list[chosen], 3))
    col2.metric("Intercept b", round(b_list[chosen], 3))
    col3.metric("Cost at the start", round(cost_list[0], 2))

    plot_area = st.empty()

    # draws the cost curve from epoch 0 up to epoch "last"
    def draw_cost(last):
        fig, ax = plt.subplots(figsize=(9, 3.8))
        ax.plot(range(last + 1), cost_list[:last + 1], color="#139A92", linewidth=2)
        ax.scatter([last], [cost_list[last]], color="#F26B21", s=60, zorder=3)
        ax.set_xlim(0, epochs)
        ax.set_ylim(0, cost_list[0] * 1.05)
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Cost")
        ax.set_title("The cost goes down as the model learns")
        ax.grid(alpha=0.3)
        return fig

    if st.button("▶ Play animation"):
        for frame in range(0, epochs + 1, 10):
            fig = draw_cost(frame)
            plot_area.pyplot(fig)
            plt.close(fig)
            time.sleep(0.05)
    else:
        fig = draw_cost(chosen)
        plot_area.pyplot(fig)
        plt.close(fig)

    # --- how the weights change ---
    st.subheader("How the weights change")
    weights_table = pd.DataFrame(w_list, columns=FACTORS)
    weights_table.insert(0, "Intercept", b_list)
    shown_epochs = [0, 1, 5, 10, 25, 50, 100, 200, 300]
    st.dataframe(weights_table.loc[shown_epochs].round(3).rename_axis("Epoch"), width="stretch")

    # --- compare with the exact matrix answer (Task 6) ---
    X_new = np.hstack([np.ones((n, 1)), X])
    exact = np.linalg.solve(X_new.T @ X_new, X_new.T @ y)
    final = np.r_[b_list[-1], w_list[-1]]
    difference = np.abs(final - exact).max()
    if difference < 0.05:
        st.success("After 300 epochs gradient descent is very close to the exact matrix solution "
                   "(largest difference " + str(round(difference, 4)) + ").")
    else:
        st.warning("After 300 epochs gradient descent is still " + str(round(difference, 3))
                   + " away from the exact solution. Try a larger learning rate.")


# ============================================================
# PAGE 10: MODEL PERFORMANCE (Task 8)
# ============================================================
if page == "📏 Model Performance":
    st.title("📏 Model performance")
    st.write("Both models are tested on " + str(len(test)) + " days that they never saw while learning.")

    # --- metrics of both models side by side ---
    mae_simple = mean_absolute_error(actual, pred_simple)
    mse_simple = mean_squared_error(actual, pred_simple)
    mae_multiple = mean_absolute_error(actual, pred_multiple)
    mse_multiple = mean_squared_error(actual, pred_multiple)

    comparison = pd.DataFrame(
        [[mae_simple, mse_simple, np.sqrt(mse_simple), r2_score(actual, pred_simple)],
         [mae_multiple, mse_multiple, np.sqrt(mse_multiple), r2_multiple]],
        index=["Simple (Humidity)", "Multiple (5 factors)"],
        columns=["MAE", "MSE", "RMSE", "R2"])
    st.subheader("Simple vs Multiple regression")
    st.dataframe(comparison.round(3), width="stretch")
    st.success("The multiple model explains " + str(round(r2_multiple * 100, 1)) + " % of the temperature change; "
               "the simple model explains only " + str(round(comparison.loc["Simple (Humidity)", "R2"] * 100, 1)) + " %.")

    # --- actual vs predicted ---
    st.subheader("Actual vs predicted")
    table = pd.DataFrame({"City": test["City"].to_numpy(), "Actual": actual,
                          "Pred_Simple": pred_simple.round(1), "Pred_Multiple": pred_multiple.round(1),
                          "Residual_Multiple": (actual - pred_multiple).round(2)})
    st.dataframe(table, width="stretch", hide_index=True)
    st.download_button("⬇️ Download predictions (CSV)", table.to_csv(index=False),
                       file_name="actual_vs_predicted.csv", mime="text/csv")

    # --- residual plots ---
    st.subheader("Residual analysis")
    st.write("Residual = actual - predicted. Below 0 means the model over-estimated, above 0 means it under-estimated.")
    model_choice = st.radio("Model", ["Multiple (5 factors)", "Simple (Humidity)"], horizontal=True)
    if model_choice == "Multiple (5 factors)":
        predicted = pred_multiple
    else:
        predicted = pred_simple
    residual = actual - predicted

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4))
    ax1.scatter(predicted, residual, s=12, color="#139A92", alpha=0.6)
    ax1.axhline(0, color="#F26B21", linestyle="--")
    ax1.set_title("Residuals vs predicted")
    ax1.set_xlabel("Predicted temperature (°C)")
    ax1.set_ylabel("Residual")
    ax2.hist(residual, bins=20, color="#139A92", edgecolor="white")
    ax2.axvline(0, color="#F26B21", linestyle="--")
    ax2.set_title("Residual distribution")
    ax2.set_xlabel("Residual (°C)")
    stats.probplot(residual, plot=ax3)
    ax3.set_title("Q-Q plot")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # --- over or under estimating? ---
    over = int((residual < 0).sum())
    under = int((residual > 0).sum())
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mean residual", str(round(residual.mean(), 3)) + " °C")
    col2.metric("Over-estimated days", over)
    col3.metric("Under-estimated days", under)
    col4.metric("Largest error", str(round(np.abs(residual).max(), 1)) + " °C")

    if abs(residual.mean()) < 0.1:
        st.success("This model is balanced. It does not over-estimate or under-estimate overall.")
    elif residual.mean() < 0:
        st.warning("This model over-estimates the temperature.")
    else:
        st.warning("This model under-estimates the temperature.")

    bands = pd.cut(actual, [0, 20, 30, 50], labels=["below 20 °C", "20 to 30 °C", "above 30 °C"])
    band_table = pd.DataFrame({"Band": bands, "Residual": residual})
    band_table = band_table.groupby("Band", observed=True)["Residual"].agg(["count", "mean"]).round(2)
    band_table.columns = ["Days", "Mean residual"]
    st.write("Mean residual for each temperature band:")
    st.dataframe(band_table, width="stretch")


# ============================================================
# PAGE 11: MAP
# ============================================================
if page == "🗺️ Map":
    st.title("🗺️ The 5 cities on the map")

    measure = st.selectbox("Show the average of", ALL_VARIABLES)
    averages = df.groupby("City")[measure].mean()

    map_table = pd.DataFrame({"City": averages.index, "Average": averages.values.round(2)})
    map_table["latitude"] = [CITY_POSITION[c][0] for c in map_table["City"]]
    map_table["longitude"] = [CITY_POSITION[c][1] for c in map_table["City"]]

    # bigger circle = bigger value
    map_table["size"] = (map_table["Average"] - map_table["Average"].min() + 0.3 * map_table["Average"].max()) * 6000

    st.map(map_table, latitude="latitude", longitude="longitude", size="size", color="#F26B21")
    st.caption("A bigger circle means a higher average value.")
    st.dataframe(map_table[["City", "Average"]].set_index("City"), width="stretch")


# ============================================================
# PAGE 12: UPLOAD YOUR OWN DATA AND RETRAIN
# ============================================================
if page == "📤 Upload Your Data":
    st.title("📤 Upload your own data")
    st.write("Upload a CSV file and the website will train both models again on your data.")
    needed = ["Humidity", "Pressure_hPa", "Sunshine_Hours", "Rainfall_mm",
              "Previous_Day_Temp", "Avg_Temperature"]
    st.write("Your file must have these columns: **" + ", ".join(needed) + "**")

    st.download_button("⬇️ Download a sample file", df[needed].head(50).to_csv(index=False),
                       file_name="sample_weather_upload.csv", mime="text/csv")

    uploaded = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded is not None:
        new_data = pd.read_csv(uploaded)
        missing_columns = [c for c in needed if c not in new_data.columns]

        if len(missing_columns) > 0:
            st.error("These columns are missing: " + ", ".join(missing_columns))
        else:
            new_data = new_data[needed].dropna()
            if len(new_data) < 30:
                st.error("Please upload at least 30 complete rows.")
            else:
                st.success(str(len(new_data)) + " complete rows loaded.")

                new_train, new_test = train_test_split(new_data, test_size=0.2, random_state=42)
                new_actual = new_test["Avg_Temperature"].to_numpy()

                new_simple = LinearRegression().fit(new_train[["Humidity"]], new_train["Avg_Temperature"])
                new_multiple = LinearRegression().fit(new_train[FACTORS], new_train["Avg_Temperature"])
                new_pred_simple = new_simple.predict(new_test[["Humidity"]])
                new_pred_multiple = new_multiple.predict(new_test[FACTORS])

                result = pd.DataFrame(
                    [[mean_absolute_error(new_actual, new_pred_simple), mean_squared_error(new_actual, new_pred_simple),
                      np.sqrt(mean_squared_error(new_actual, new_pred_simple)), r2_score(new_actual, new_pred_simple)],
                     [mean_absolute_error(new_actual, new_pred_multiple), mean_squared_error(new_actual, new_pred_multiple),
                      np.sqrt(mean_squared_error(new_actual, new_pred_multiple)), r2_score(new_actual, new_pred_multiple)]],
                    index=["Simple (Humidity)", "Multiple (5 factors)"],
                    columns=["MAE", "MSE", "RMSE", "R2"])
                st.subheader("Results on your data")
                st.dataframe(result.round(3), width="stretch")

                weights = pd.DataFrame({"Weight": new_multiple.coef_}, index=FACTORS).round(4)
                st.write("Intercept: **" + str(round(new_multiple.intercept_, 3)) + "**")
                st.dataframe(weights, width="stretch")

                fig, ax = plt.subplots(figsize=(6, 4))
                ax.scatter(new_actual, new_pred_multiple, s=14, color="#139A92")
                low, high = new_actual.min(), new_actual.max()
                ax.plot([low, high], [low, high], color="#F26B21", linestyle="--", label="perfect prediction")
                ax.set_xlabel("Actual temperature (°C)")
                ax.set_ylabel("Predicted temperature (°C)")
                ax.legend()
                st.pyplot(fig)
                plt.close(fig)
