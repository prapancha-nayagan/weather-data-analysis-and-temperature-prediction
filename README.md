# Weather Data Analysis and Temperature Prediction

Statistical and mathematical analysis of 1,000 daily weather records from five Indian cities
(Chennai, Delhi, Mumbai, Bengaluru, Kolkata), ending in a regression model that predicts
average daily temperature.

## Folder contents
| File | Purpose |
|---|---|
| `generate_dataset.py` | Creates `data/weather_data.csv` (raw data with missing values, duplicates, errors) |
| `task1_data_preprocessing.py` | Load, clean, find numerical/categorical variables; saves `data/weather_clean.csv` |
| `task2_descriptive_inferential.py` | Mean/median/mode, variance, std, distribution, sampling, hypothesis tests |
| `task3_probability.py` | Probability, conditional probability, Bayes' theorem, law of large numbers |
| `task4_correlation.py` | Pearson, Spearman, correlation matrix, strongest factors |
| `task5_regression.py` | Simple vs multiple linear regression and comparison |
| `task6_linear_algebra.py` | Vectors, matrices, dot product, normal equation |
| `task7_gradient_descent.py` | Cost function, derivatives, gradient descent |
| `task8_model_evaluation.py` | MAE, MSE, RMSE, R² for both models side by side, residual analysis |
| `app.py` | The website (Streamlit): run with `streamlit run app.py` |
| `outputs/` | Chart pictures used in the presentation |
| `presentation/` | The PowerPoint deck (and the script that builds it) |

## How to run
```
pip install -r requirements.txt
python generate_dataset.py      # only needed once
python task1_data_preprocessing.py   # run first: creates the clean data
python task2_descriptive_inferential.py
... up to task8_model_evaluation.py
```
Run the scripts in order. Tasks 2, 3, 4, 5, 7 and 8 draw graphs, and each graph opens in a window.
Close the graph window to let the program continue. (The programs do not save the graphs; the
pictures already in `outputs/` are only the ones used in the presentation.)

## Dataset columns
Record_ID, City, Date, Humidity, Rainfall_mm, Wind_Speed, Pressure_hPa, Cloud_Cover,
Sunshine_Hours, Previous_Day_Temp, Rain_Today, Avg_Temperature (target).

The data is synthetic (generated with a fixed random seed) but follows realistic seasonal,
monsoon and city-level climate patterns.

## Rebuilding the presentation (optional)
The finished deck is `presentation/Weather_Data_Analysis_Presentation.pptx`.
To regenerate it with `presentation/build_deck.js` (needs Node.js from nodejs.org):
```
cd presentation
npm install
node build_deck.js
```
The chart pictures it needs are already in `outputs/`.

## The website (localhost)
```
pip install -r requirements.txt
python task1_data_preprocessing.py      # once, creates data/weather_clean.csv
streamlit run app.py
```
It opens at http://localhost:8501 with 12 pages: Project Info, Dataset (filters, download),
Trends, City Comparison, Predict Temperature (range, explanation, what-if), Probability
Calculator, Correlation, Hypothesis Test, Gradient Descent (with animation), Model Performance,
Map, and Upload Your Data (retrain on your own CSV).
For dark/light theme use the top-right menu: Settings -> Theme.
