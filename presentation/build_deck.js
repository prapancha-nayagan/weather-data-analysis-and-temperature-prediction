const pptxgen = require("pptxgenjs");
const sharp = require("sharp");
const path = require("path");
const { applyTheme } = require("./apply_theme.js");   // helper file in this folder

const THEME = {
  name: "Weather Analysis", headFontFace: "Calibri", bodyFontFace: "Calibri",
  colors: { dk1: "1B2040", lt1: "FFFFFF", dk2: "2A3160", lt2: "F1F3F8",
    accent1: "F26B21", accent2: "139A92", accent3: "6F5FE0", accent4: "D93F4A",
    accent5: "E8A317", accent6: "5B6385", hlink: "139A92", folHlink: "6F5FE0" },
};
// chart images made by the task programs (the "outputs" folder next to this folder)
const OUT = path.join(__dirname, "..", "outputs") + "/";
const FILE = path.join(__dirname, "Weather_Data_Analysis_Presentation.pptx");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.theme = { headFontFace: "Calibri", bodyFontFace: "Calibri" };
pres.title = "Weather Data Analysis and Temperature Prediction";
const C = pres.SchemeColor;
const NAVY = "1B2040", ORANGE = "F26B21", TEAL = "139A92";

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "TITLE_DARK", background: { color: NAVY },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.0, w: 8.2, h: 2.2, fontSize: 46, bold: true, color: C.background1, align: "left", valign: "top", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 4.4, w: 7.6, h: 1.2, fontSize: 18, color: C.background2, align: "left", valign: "top", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT_LIGHT", background: { color: "FFFFFF" },
  slideNumber: { x: 12.1, y: 7.05, w: 0.6, h: 0.3, fontSize: 10, color: "5B6385", align: "right" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.4, w: 12.1, h: 0.8, fontSize: 34, bold: true, color: C.text1, align: "left", valign: "middle", margin: 0 }, text: "" } },
    { text: { text: "Weather Data Analysis and Temperature Prediction", options: { x: 0.6, y: 7.05, w: 8, h: 0.3, fontSize: 10, color: C.accent6, margin: 0 } } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT_DARK", background: { color: NAVY },
  slideNumber: { x: 12.1, y: 7.05, w: 0.6, h: 0.3, fontSize: 10, color: "B9C0DC", align: "right" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.4, w: 12.1, h: 0.8, fontSize: 34, bold: true, color: C.background1, align: "left", valign: "middle", margin: 0 }, text: "" } },
  ],
});

// ---------- helpers ----------
async function img(slide, file, x, y, w, h, name) {
  const m = await sharp(OUT + file).metadata();
  const s = Math.min(w / m.width, h / m.height);
  const iw = m.width * s, ih = m.height * s;
  slide.addImage({ path: OUT + file, x: x + (w - iw) / 2, y: y + (h - ih) / 2, w: iw, h: ih, altText: name, objectName: name });
}
function card(slide, x, y, w, h, name, fill) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill || C.background2 }, line: { type: "none" }, objectName: name });
}
function stat(slide, x, y, w, h, big, label, color, name) {
  card(slide, x, y, w, h, name + " card");
  slide.addText(big, { x: x + 0.15, y: y + 0.12, w: w - 0.3, h: h * 0.52, fontSize: 32, bold: true, color: color || C.accent1, align: "left", valign: "middle", margin: 0, isTextBox: true, objectName: name + " value" });
  slide.addText(label, { x: x + 0.15, y: y + h * 0.58, w: w - 0.3, h: h * 0.36, fontSize: 14, color: C.text1, align: "left", valign: "top", margin: 0, isTextBox: true, objectName: name + " label" });
}
function badge(slide, x, y, n, color, name) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: 0.5, h: 0.5, fill: { color }, line: { type: "none" }, objectName: name + " circle" });
  slide.addText(String(n), { x, y, w: 0.5, h: 0.5, fontSize: 18, bold: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: name + " number" });
}
function code(slide, x, y, w, h, lines, name) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: C.text1 }, line: { type: "none" }, objectName: name + " panel" });
  const runs = lines.map((l, i) => ({ text: l, options: { breakLine: i < lines.length - 1 } }));
  slide.addText(runs, { x: x + 0.2, y: y + 0.12, w: w - 0.4, h: h - 0.24, fontFace: "Courier New", fontSize: 12, color: "E6E9F5", align: "left", valign: "top", margin: 0, isTextBox: true, objectName: name });
}
function bullets(slide, x, y, w, h, items, name, size) {
  const runs = items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: 8 } }));
  slide.addText(runs, { x, y, w, h, fontSize: size || 16, color: C.text1, align: "left", valign: "top", margin: 0, isTextBox: true, objectName: name });
}
function label(slide, text, x, y, w, color, name) {
  slide.addText(text, { x, y, w, h: 0.35, fontSize: 14, bold: true, color: color || C.accent1, align: "left", valign: "middle", margin: 0, isTextBox: true, objectName: name });
}
const hdr = (t) => ({ text: t, options: { bold: true, color: C.background1, fill: { color: C.text1 }, fontSize: 14 } });
const cell = (t, o) => ({ text: String(t), options: Object.assign({ fontSize: 14, color: C.text1 }, o || {}) });

(async () => {
  // ===== 1. Title =====
  pres.addSection({ title: "Introduction" });
  let s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Introduction" });
  s.addText("Weather Data Analysis and Temperature Prediction", { placeholder: "title" });
  s.addText("Statistical and mathematical techniques applied to 1,000 daily weather records from five Indian cities", { placeholder: "body" });
  const chips = [["1,000", "daily records"], ["5", "Indian cities"], ["8", "analysis tasks"]];
  chips.forEach((c, i) => {
    const y = 1.6 + i * 1.7;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 9.3, y, w: 3.3, h: 1.4, rectRadius: 0.12, fill: { color: "2A3160" }, line: { type: "none" }, objectName: "chip " + i });
    s.addText(c[0], { x: 9.5, y: y + 0.1, w: 2.9, h: 0.75, fontSize: 40, bold: true, color: i === 1 ? C.accent2 : C.accent1, margin: 0, valign: "middle", isTextBox: true, objectName: "chip value " + i });
    s.addText(c[1], { x: 9.5, y: y + 0.85, w: 2.9, h: 0.4, fontSize: 16, color: C.background2, margin: 0, isTextBox: true, objectName: "chip label " + i });
  });
  s.addNotes("Welcome. This project analyses daily weather data from Chennai, Delhi, Mumbai, Bengaluru and Kolkata and builds a model that predicts the average daily temperature. It follows the eight-task workflow from the project document and uses ideas from the four course units: descriptive statistics, inferential statistics, probability, and linear algebra.");

  // ===== 2. Problem & objectives =====
  s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Introduction" });
  s.addText("Problem statement and objectives", { placeholder: "title" });
  const cols = [
    ["Problem", C.accent1, "Daily temperature depends on humidity, pressure, sunshine, rain and how hot the previous day was. Which factors matter most, and can we predict temperature from them?"],
    ["Objective", C.accent2, "Analyse the factors that influence temperature, find significant relationships, and build regression models that predict average daily temperature."],
    ["Approach", C.accent3, "Clean the data, describe it, test ideas with probability and hypothesis tests, measure correlation, fit regression, then evaluate the model with error metrics and residuals."],
  ];
  cols.forEach((c, i) => {
    const x = 0.6 + i * 4.12;
    card(s, x, 1.6, 3.9, 4.9, "card " + c[0]);
    badge(s, x + 0.3, 1.9, i + 1, c[1], "badge " + c[0]);
    s.addText(c[0], { x: x + 0.3, y: 2.6, w: 3.3, h: 0.5, fontSize: 24, bold: true, color: C.text1, margin: 0, isTextBox: true, objectName: "heading " + c[0] });
    s.addText(c[2], { x: x + 0.3, y: 3.25, w: 3.3, h: 3.0, fontSize: 16, color: C.text1, valign: "top", margin: 0, isTextBox: true, objectName: "text " + c[0] });
  });
  s.addNotes("The problem is simple to state: what drives temperature, and can we predict it? The objective mirrors the student-performance template in the project document, but adapted to weather: instead of predicting final marks we predict average temperature.");

  // ===== 3. Workflow =====
  s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Introduction" });
  s.addText("Project workflow: eight tasks", { placeholder: "title" });
  const tasks = [
    ["Data preprocessing", "Load, fix missing values, remove duplicates"],
    ["Descriptive and inferential statistics", "Mean, spread, sampling, hypothesis tests"],
    ["Probability analysis", "Conditional probability, Bayes, law of large numbers"],
    ["Correlation analysis", "Pearson, Spearman, correlation matrix"],
    ["Regression analysis", "Simple and multiple linear regression"],
    ["Linear algebra", "Vectors, matrices, normal equation"],
    ["Calculus and optimisation", "Cost function, derivatives, gradient descent"],
    ["Model evaluation", "MAE, MSE, RMSE, R², residuals"],
  ];
  const tcol = [C.accent1, C.accent2, C.accent3, C.accent1, C.accent2, C.accent3, C.accent1, C.accent2];
  tasks.forEach((t, i) => {
    const x = 0.6 + (i % 4) * 3.07, y = 1.6 + Math.floor(i / 4) * 2.65;
    card(s, x, y, 2.9, 2.45, "task card " + (i + 1));
    badge(s, x + 0.2, y + 0.2, i + 1, tcol[i], "task badge " + (i + 1));
    s.addText(t[0], { x: x + 0.2, y: y + 0.85, w: 2.5, h: 0.65, fontSize: 16, bold: true, color: C.text1, valign: "top", margin: 0, isTextBox: true, objectName: "task title " + (i + 1) });
    s.addText(t[1], { x: x + 0.2, y: y + 1.5, w: 2.5, h: 0.8, fontSize: 14, color: C.accent6, valign: "top", margin: 0, isTextBox: true, objectName: "task text " + (i + 1) });
  });
  s.addNotes("Each task has its own Python program, task1 to task8, and each program is short, commented and prints its results. Tasks run in order because task 1 saves the cleaned dataset that all later tasks read.");

  // ===== 4. Dataset =====
  s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Introduction" });
  s.addText("The dataset: Indian daily weather records", { placeholder: "title" });
  const feat = [
    ["Record_ID", "Unique record ID", "Identifier"],
    ["City", "Chennai, Delhi, Mumbai, Bengaluru, Kolkata", "Categorical"],
    ["Date", "Observation date (2023)", "Date"],
    ["Humidity", "Relative humidity (%)", "Numerical"],
    ["Rainfall_mm", "Rainfall that day (mm)", "Numerical"],
    ["Wind_Speed", "Wind speed (km/h)", "Numerical"],
    ["Pressure_hPa", "Air pressure (hPa)", "Numerical"],
    ["Cloud_Cover", "Sky covered by cloud (%)", "Numerical"],
    ["Sunshine_Hours", "Hours of sunshine", "Numerical"],
    ["Previous_Day_Temp", "Previous day's temperature (°C)", "Numerical"],
    ["Rain_Today", "Yes if rainfall above 2.5 mm", "Categorical"],
    ["Avg_Temperature", "Target: average temperature (°C)", "Numerical"],
  ];
  const rows = [[hdr("Feature"), hdr("Description"), hdr("Type")]].concat(feat.map((f, i) => {
    const t = i === feat.length - 1;
    const o = { fill: { color: t ? C.accent1 : (i % 2 ? C.background2 : C.background1) }, bold: t, color: t ? C.background1 : C.text1 };
    return [cell(f[0], o), cell(f[1], o), cell(f[2], o)];
  }));
  s.addTable(rows, { x: 0.6, y: 1.5, w: 8.4, colW: [2.4, 4.2, 1.8], rowH: 0.42, border: { type: "solid", pt: 0.5, color: "D5D9E6" }, valign: "middle", objectName: "dataset table" });
  stat(s, 9.4, 1.5, 3.3, 1.5, "1,015", "raw rows, 12 columns", C.accent1, "stat raw");
  stat(s, 9.4, 3.2, 3.3, 1.5, "1,000", "rows after cleaning", C.accent2, "stat clean");
  card(s, 9.4, 4.9, 3.3, 1.65, "dirt card");
  s.addText("Added on purpose for Task 1: 71 missing values, 15 duplicate rows and 4 impossible humidity readings.", { x: 9.55, y: 5.0, w: 3.0, h: 1.45, fontSize: 14, color: C.text1, valign: "middle", margin: 0, isTextBox: true, objectName: "dirt text" });
  s.addNotes("The dataset is synthetic but follows real climate patterns: each city has its own average temperature and seasonal swing, the monsoon months bring rain and cloud, and humidity falls when temperature rises. It was generated by generate_dataset.py with a fixed random seed so results are reproducible. 1,000 clean records, in the 500 to 1,000 plus range the project document asks for.");

  // ===== 5. Task 1 =====
  pres.addSection({ title: "Analysis" });
  s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Analysis" });
  s.addText("Task 1: Data preprocessing", { placeholder: "title" });
  stat(s, 0.6, 1.6, 2.9, 1.5, "71", "missing values filled with the median", C.accent1, "t1 missing");
  stat(s, 3.7, 1.6, 2.9, 1.5, "15", "duplicate rows removed", C.accent2, "t1 dup");
  stat(s, 0.6, 3.3, 2.9, 1.5, "4", "humidity readings above 100 % corrected", C.accent3, "t1 humidity");
  stat(s, 3.7, 3.3, 2.9, 1.5, "0", "missing values left", C.accent1, "t1 zero");
  card(s, 0.6, 5.0, 6.0, 1.55, "t1 types card");
  s.addText([
    { text: "Numerical: ", options: { bold: true } }, { text: "Humidity, Rainfall, Wind, Pressure, Cloud, Sunshine, temperatures", options: { breakLine: true } },
    { text: "Categorical: ", options: { bold: true } }, { text: "City, Rain_Today" },
  ], { x: 0.8, y: 5.1, w: 5.6, h: 1.35, fontSize: 14, color: C.text1, valign: "middle", margin: 0, isTextBox: true, objectName: "t1 types" });
  code(s, 6.9, 1.6, 5.8, 4.95, [
    "df = pd.read_csv(\"data/weather_data.csv\")",
    "",
    "# remove duplicate records",
    "df = df.drop_duplicates()",
    "",
    "# humidity cannot be above 100 %",
    "bad = df[\"Humidity\"] > 100",
    "df.loc[bad, \"Humidity\"] = np.nan",
    "",
    "# fill gaps with the median",
    "for col in numeric_cols:",
    "    df[col] = df[col].fillna(",
    "        df[col].median())",
    "",
    "df.to_csv(\"data/weather_clean.csv\")",
  ], "t1 code");
  s.addNotes("Real data is messy. We found 15 duplicate rows, 71 missing values, and four humidity values above 100 percent, which is physically impossible. We marked those as missing, then filled every gap with the median because the median is not pulled around by extreme values. The cleaned file is saved for the next tasks.");

  // ===== 6. Task 2 descriptive =====
  s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Analysis" });
  s.addText("Task 2: Descriptive statistics of temperature", { placeholder: "title" });
  const dstats = [["25.93 °C", "Mean", C.accent1], ["26.10 °C", "Median", C.accent2], ["25.9 °C", "Mode", C.accent3],
    ["4.62 °C", "Standard deviation", C.accent1], ["21.35", "Variance", C.accent2], ["−0.17", "Skewness", C.accent3]];
  dstats.forEach((d, i) => stat(s, 0.6 + (i % 2) * 2.55, 1.6 + Math.floor(i / 2) * 1.65, 2.4, 1.5, d[0], d[1], d[2], "t2 stat " + (i + 1)));
  await img(s, "task2_distribution.png", 5.9, 1.6, 6.8, 3.2, "Temperature histogram and boxplot by city");
  card(s, 5.9, 5.0, 6.8, 1.55, "t2 insight card");
  s.addText("Mean and median are almost equal and skewness is near zero, so temperatures are roughly symmetric. Delhi has the widest spread (std 7.1 °C) and Chennai the warmest average (28.4 °C).", { x: 6.1, y: 5.05, w: 6.4, h: 1.45, fontSize: 14, color: C.text1, valign: "middle", margin: 0, isTextBox: true, objectName: "t2 insight" });
  s.addNotes("The mean of 25.9 and median of 26.1 are very close and skewness is near zero, so the distribution is roughly bell shaped. The box plot shows the cities differ a lot: Delhi swings between cool winters and very hot summers, while Chennai and Mumbai stay stable.");

  // ===== 7. Task 2 inferential =====
  s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Analysis" });
  s.addText("Task 2: Sampling and hypothesis testing", { placeholder: "title" });
  label(s, "SAMPLING: how close is each sample to the true mean?", 0.6, 1.5, 6, C.accent1, "t2 sampling label");
  const samp = [["Method", "Sample mean (°C)"], ["Population (1,000 days)", "25.93"], ["Simple random (100)", "26.02"], ["Stratified by city (100)", "25.36"], ["Systematic, every 10th (100)", "26.72"]];
  s.addTable(samp.map((r, i) => r.map((t, j) => i === 0 ? hdr(t) : cell(t, { fill: { color: i % 2 ? C.background2 : C.background1 }, bold: i === 1, align: j ? "right" : "left" }))),
    { x: 0.6, y: 1.95, w: 5.9, colW: [3.9, 2.0], rowH: 0.48, border: { type: "solid", pt: 0.5, color: "D5D9E6" }, valign: "middle", objectName: "sampling table" });
  card(s, 0.6, 4.6, 5.9, 1.95, "ci card");
  s.addText([
    { text: "95% confidence interval", options: { bold: true, breakLine: true } },
    { text: "The simple random sample puts the true mean between 25.13 and 26.90 °C, and the true mean 25.93 °C lies inside it." },
  ], { x: 0.8, y: 4.7, w: 5.5, h: 1.75, fontSize: 14, color: C.text1, valign: "middle", margin: 0, isTextBox: true, objectName: "ci text" });

  label(s, "HYPOTHESIS TESTS (significance level 0.05)", 6.9, 1.5, 6, C.accent2, "t2 test label");
  card(s, 6.9, 1.95, 5.8, 2.2, "test1 card");
  s.addText([
    { text: "Rainy vs dry days (t-test)", options: { bold: true, breakLine: true } },
    { text: "Rainy 25.46 °C, dry 26.04 °C", options: { breakLine: true } },
    { text: "t = −1.66, p = 0.097", options: { breakLine: true } },
    { text: "p > 0.05: fail to reject H0, so no significant difference.", options: { bold: true, color: C.accent1 } },
  ], { x: 7.1, y: 2.0, w: 5.4, h: 2.1, fontSize: 14, color: C.text1, valign: "middle", margin: 0, isTextBox: true, paraSpaceAfter: 4, objectName: "test1 text" });
  card(s, 6.9, 4.35, 5.8, 2.2, "test2 card");
  s.addText([
    { text: "Five cities (one-way ANOVA)", options: { bold: true, breakLine: true } },
    { text: "H0: all cities have the same mean temperature", options: { breakLine: true } },
    { text: "F = 34.15, p < 0.001", options: { breakLine: true } },
    { text: "p < 0.05: reject H0, so cities differ significantly.", options: { bold: true, color: C.accent2 } },
  ], { x: 7.1, y: 4.4, w: 5.4, h: 2.1, fontSize: 14, color: C.text1, valign: "middle", margin: 0, isTextBox: true, paraSpaceAfter: 4, objectName: "test2 text" });
  s.addNotes("Sampling: three ways to draw 100 days. All land near the true mean of 25.93; the simple random sample is closest. Hypothesis test one: is it cooler on rainy days? The p-value is 0.097, above 0.05, so we cannot claim a real difference. Hypothesis test two: do cities differ? The ANOVA p-value is essentially zero, so yes, location matters a lot.");

  // ===== 8. Task 3 probability =====
  s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Analysis" });
  s.addText("Task 3: Probability analysis", { placeholder: "title" });
  const pc = [
    ["Probability of a hot day", "0.199", "P(Temperature > 30 °C)", "199 hot days out of 1,000", C.accent1],
    ["Conditional probability", "0.632", "P(Hot | Humidity < 60 %)", "Dry air makes a hot day 3.2 times as likely.", C.accent2],
    ["Bayes' theorem", "0.554", "P(Rain | Cloudy) = P(Cloudy | Rain) × P(Rain) / P(Cloudy)", "A cloudy sky (cloud cover > 60 %) lifts the chance of rain from 18.4 % to 55.4 %.", C.accent3],
  ];
  pc.forEach((p, i) => {
    const x = 0.6 + i * 4.12;
    card(s, x, 1.6, 3.9, 4.95, "prob card " + (i + 1));
    label(s, p[0].toUpperCase(), x + 0.3, 1.85, 3.3, p[4], "prob label " + (i + 1));
    s.addText(p[1], { x: x + 0.3, y: 2.3, w: 3.3, h: 1.2, fontSize: 60, bold: true, color: p[4], margin: 0, valign: "middle", isTextBox: true, objectName: "prob value " + (i + 1) });
    s.addText(p[2], { x: x + 0.3, y: 3.65, w: 3.3, h: 0.95, fontSize: 14, bold: true, color: C.text1, margin: 0, valign: "top", isTextBox: true, objectName: "prob formula " + (i + 1) });
    s.addText(p[3], { x: x + 0.3, y: 4.75, w: 3.3, h: 1.6, fontSize: 14, color: C.text1, margin: 0, valign: "top", isTextBox: true, objectName: "prob meaning " + (i + 1) });
  });
  s.addNotes("Three probability ideas. First, a simple probability: about one day in five is hotter than 30 degrees. Second, conditional probability: if we only look at days with humidity below 60 percent, the chance of a hot day jumps to 63 percent. Third, Bayes' theorem: we start with an 18 percent chance of rain, observe a cloudy sky, and update to 55 percent. The program also checks Bayes against a direct count and gets the same number.");

  // ===== 9. Law of large numbers =====
  s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Analysis" });
  s.addText("Task 3: Law of large numbers", { placeholder: "title" });
  await img(s, "task3_law_of_large_numbers.png", 0.6, 1.5, 7.4, 4.1, "Running mean converging to population mean");
  s.addText("The running average of a growing sample settles on the true mean.", { x: 0.6, y: 5.75, w: 7.4, h: 0.7, fontSize: 14, color: C.accent6, margin: 0, valign: "top", isTextBox: true, objectName: "lln caption" });
  s.addTable([[hdr("Sample size"), hdr("Sample mean"), hdr("Error")]].concat(
    [["10", "25.31", "0.63"], ["50", "25.62", "0.32"], ["100", "25.58", "0.35"], ["500", "25.73", "0.20"], ["1,000", "25.83", "0.11"]].map((r, i) => r.map((t, j) => cell(t, { fill: { color: i % 2 ? C.background1 : C.background2 }, align: j ? "right" : "left" })))),
    { x: 8.4, y: 1.6, w: 4.3, colW: [1.5, 1.5, 1.3], rowH: 0.5, border: { type: "solid", pt: 0.5, color: "D5D9E6" }, valign: "middle", objectName: "lln table" });
  card(s, 8.4, 5.0, 4.3, 1.55, "lln card");
  s.addText("True mean: 25.94 °C. With 10 days the error is 0.63 °C; with 1,000 days it is 0.11 °C.", { x: 8.6, y: 5.05, w: 3.9, h: 1.45, fontSize: 14, color: C.text1, valign: "middle", margin: 0, isTextBox: true, objectName: "lln text" });
  s.addNotes("The law of large numbers says more observations bring the sample average closer to the true average. We resampled the temperatures and tracked the running mean: after ten days it is off by 0.63 degrees, after a thousand days by only 0.11.");

  // ===== 10. Correlation =====
  s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Analysis" });
  s.addText("Task 4: Correlation analysis", { placeholder: "title" });
  const cn = ["Previous_Day_Temp", "Humidity", "Pressure_hPa", "Sunshine_Hours", "Rainfall_mm", "Cloud_Cover", "Wind_Speed"];
  const cv = [0.958, -0.560, -0.376, 0.234, -0.055, -0.055, -0.011];
  s.addChart(pres.charts.BAR, [{ name: "Pearson r", labels: cn, values: cv }], {
    x: 0.6, y: 1.5, w: 6.2, h: 4.2, barDir: "bar", chartColors: [TEAL], invertedColors: ["D93F4A"], barGapWidthPct: 50,
    showTitle: true, title: "Pearson correlation with temperature", titleFontSize: 14, titleColor: NAVY, titleFontFace: "+mn-lt",
    showValue: true, dataLabelFormatCode: "0.00", dataLabelFontSize: 12, dataLabelColor: NAVY, dataLabelFontFace: "+mn-lt", dataLabelPosition: "outEnd",
    catAxisOrientation: "maxMin", catAxisLabelColor: NAVY, catAxisLabelFontSize: 12, catAxisLabelFontFace: "+mn-lt", catAxisLabelPos: "low",
    valAxisLabelColor: "5B6385", valAxisLabelFontSize: 12, valAxisLabelFontFace: "+mn-lt", valAxisMinVal: -1, valAxisMaxVal: 1, valAxisLabelFormatCode: "0.0",
    valGridLine: { color: "E3E6F0", size: 0.5 }, catGridLine: { style: "none" }, showLegend: false,
  });
  s.addText("Teal = positive, red = negative. Spearman values match closely (for example 0.953 for Previous_Day_Temp).", { x: 0.6, y: 5.75, w: 6.2, h: 0.75, fontSize: 14, color: C.accent6, margin: 0, valign: "top", isTextBox: true, objectName: "corr caption" });
  await img(s, "task4_correlation_matrix.png", 7.0, 1.5, 5.7, 5.0, "Correlation matrix heatmap");
  s.addNotes("Pearson measures straight-line relationships and Spearman measures rank relationships; both agree here. The strongest factor by far is yesterday's temperature at 0.96. Then humidity is moderately negative, because hotter days are drier, and pressure is weakly negative. Wind speed, cloud cover and rainfall have almost no direct linear relationship with temperature. The heat map also shows cloud cover and sunshine are strongly negatively related to each other.");

  // ===== 11. Regression =====
  s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Analysis" });
  s.addText("Task 5: Simple vs multiple linear regression", { placeholder: "title" });
  card(s, 0.6, 1.5, 4.5, 2.4, "model1 card");
  label(s, "MODEL 1: SIMPLE (HUMIDITY)", 0.8, 1.6, 4.1, C.accent1, "model1 label");
  s.addText([{ text: "R² = 0.276", options: { bold: true, fontSize: 28, color: C.accent1, breakLine: true } }, { text: "RMSE = 4.17 °C", options: { fontSize: 16, breakLine: true } }, { text: "Temp = 40.56 − 0.194 × Humidity", options: { fontSize: 14 } }],
    { x: 0.8, y: 2.0, w: 4.1, h: 1.8, color: C.text1, valign: "top", margin: 0, isTextBox: true, paraSpaceAfter: 4, objectName: "model1 text" });
  card(s, 0.6, 4.1, 4.5, 2.45, "model2 card");
  label(s, "MODEL 2: MULTIPLE (5 FACTORS)", 0.8, 4.2, 4.1, C.accent2, "model2 label");
  s.addText([{ text: "R² = 0.939", options: { bold: true, fontSize: 28, color: C.accent2, breakLine: true } }, { text: "RMSE = 1.21 °C", options: { fontSize: 16, breakLine: true } }, { text: "Humidity, pressure, sunshine, rainfall, previous-day temperature", options: { fontSize: 14 } }],
    { x: 0.8, y: 4.6, w: 4.1, h: 1.9, color: C.text1, valign: "top", margin: 0, isTextBox: true, paraSpaceAfter: 4, objectName: "model2 text" });
  await img(s, "task5_regression_models.png", 5.3, 1.5, 7.4, 3.5, "Simple and multiple regression plots");
  card(s, 5.3, 5.15, 7.4, 1.4, "reg insight card");
  s.addText("The multiple model explains 93.9 % of temperature variation against 27.6 % for humidity alone. Previous-day temperature carries most of that gain (coefficient 0.87).", { x: 5.5, y: 5.2, w: 7.0, h: 1.3, fontSize: 14, color: C.text1, valign: "middle", margin: 0, isTextBox: true, objectName: "reg insight" });
  s.addNotes("We split the data 80/20: 800 days to train, 200 unseen days to test. The simple model uses only humidity and explains about 28 percent of the variation. The multiple model uses five factors and explains 94 percent, with a typical error of about 1.2 degrees. On the right, the second plot shows predictions hugging the perfect-prediction line.");

  // ===== 12. Linear algebra =====
  s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Analysis" });
  s.addText("Task 6: Linear algebra behind regression", { placeholder: "title" });
  bullets(s, 0.6, 1.6, 5.6, 2.4, [
    "One day of weather is a vector of 5 numbers.",
    "All 1,000 days form a matrix X of shape 1000 × 5.",
    "Dot product: multiply matching numbers and add them up. X @ weights predicts every day at once.",
  ], "la bullets", 16);
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 4.2, w: 5.6, h: 1.1, rectRadius: 0.1, fill: { color: C.text1 }, line: { type: "none" }, objectName: "formula panel" });
  s.addText("β = (XᵀX)⁻¹ Xᵀ y", { x: 0.6, y: 4.2, w: 5.6, h: 1.1, fontSize: 30, bold: true, italic: true, color: C.background1, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "formula text" });
  s.addText("The normal equation gives the best coefficients directly. Result matches scikit-learn: True.", { x: 0.6, y: 5.5, w: 5.6, h: 1.0, fontSize: 14, color: C.accent6, margin: 0, valign: "top", isTextBox: true, objectName: "la caption" });
  code(s, 6.5, 1.6, 6.2, 2.75, [
    "X_b = np.hstack([ones, X])  # add intercept",
    "",
    "XtX = X_b.T @ X_b           # 6 x 6 matrix",
    "Xty = X_b.T @ y",
    "",
    "beta = np.linalg.inv(XtX) @ Xty",
    "predicted = X_b @ beta",
  ], "la code");
  s.addTable([[hdr("Coefficient"), hdr("Value")]].concat(
    [["Intercept", "157.13"], ["Humidity", "−0.043"], ["Pressure_hPa", "−0.149"], ["Sunshine_Hours", "−0.054"], ["Rainfall_mm", "−0.021"], ["Previous_Day_Temp", "0.869"]].map((r, i) => r.map((t, j) => cell(t, { fill: { color: i % 2 ? C.background1 : C.background2 }, align: j ? "right" : "left", fontSize: 13 })))),
    { x: 6.5, y: 4.5, w: 6.2, colW: [3.9, 2.3], rowH: 0.29, border: { type: "solid", pt: 0.5, color: "D5D9E6" }, valign: "middle", objectName: "beta table" });
  s.addNotes("Regression is really matrix algebra. Each day is a vector, the whole dataset is a matrix, and a prediction is a dot product between the weights and the day's features. The normal equation, beta equals X-transpose-X inverse times X-transpose y, solves for the best weights in one step. We checked it against scikit-learn and the coefficients match.");

  // ===== 13. Gradient descent =====
  s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Analysis" });
  s.addText("Task 7: Calculus and gradient descent", { placeholder: "title" });
  await img(s, "task7_gradient_descent.png", 0.6, 1.5, 7.4, 3.2, "Cost curve and learning rate comparison");
  card(s, 0.6, 4.9, 7.4, 1.65, "gd formula card");
  s.addText([
    { text: "Cost: J = (1/2n) Σ (prediction − actual)²", options: { breakLine: true } },
    { text: "Slope: dJ/dw = (1/n) Xᵀ (prediction − actual)", options: { breakLine: true } },
    { text: "Step: w = w − learning rate × dJ/dw", options: { bold: true } },
  ], { x: 0.8, y: 4.95, w: 7.0, h: 1.55, fontSize: 16, color: C.text1, valign: "middle", margin: 0, isTextBox: true, paraSpaceAfter: 4, objectName: "gd formulas" });
  s.addTable([[hdr("Epoch"), hdr("Cost"), hdr("Intercept b")]].concat(
    [["0", "346.97", "0.00"], ["10", "42.40", "16.89"], ["50", "0.785", "25.80"], ["200", "0.748", "25.94"]].map((r, i) => r.map((t, j) => cell(t, { fill: { color: i % 2 ? C.background1 : C.background2 }, align: j ? "right" : "left" })))),
    { x: 8.4, y: 1.6, w: 4.3, colW: [1.2, 1.4, 1.7], rowH: 0.5, border: { type: "solid", pt: 0.5, color: "D5D9E6" }, valign: "middle", objectName: "gd table" });
  card(s, 8.4, 4.3, 4.3, 2.25, "gd insight card");
  s.addText("Cost falls from 347 to 0.75 and the parameters settle at the exact matrix solution. A learning rate of 0.01 is too slow; 0.1 and 0.5 converge quickly.", { x: 8.6, y: 4.35, w: 3.9, h: 2.15, fontSize: 14, color: C.text1, valign: "middle", margin: 0, isTextBox: true, objectName: "gd insight" });
  s.addNotes("The cost function measures how wrong the model is. Its derivative tells us which direction reduces the error, and gradient descent repeatedly steps downhill. The table shows the cost dropping and the intercept moving from zero to 25.9, the average temperature. The right chart compares learning rates: too small is slow, larger is faster. The features are standardised first so all weights move at a similar speed.");

  // ===== 14. Evaluation =====
  s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Analysis" });
  s.addText("Task 8: Model evaluation and residual analysis", { placeholder: "title" });
  const evalRows = [["Simple (Humidity)", "3.34", "17.37", "4.17", "0.276"], ["Multiple (5 factors)", "0.97", "1.48", "1.21", "0.939"]];
  s.addTable([[hdr("Model (200 test days)"), hdr("MAE (°C)"), hdr("MSE"), hdr("RMSE (°C)"), hdr("R²")]].concat(
    evalRows.map((r, i) => r.map((t, j) => cell(t, { fill: { color: i ? C.background2 : C.background1 }, bold: i === 1, color: i === 1 ? C.accent2 : C.text1, align: j ? "right" : "left", fontSize: 16 })))),
    { x: 0.6, y: 1.4, w: 12.1, colW: [3.7, 2.1, 2.1, 2.1, 2.1], rowH: 0.5, border: { type: "solid", pt: 0.5, color: "D5D9E6" }, valign: "middle", objectName: "metrics table" });
  await img(s, "task8_residual_analysis.png", 0.6, 3.1, 7.4, 3.8, "Residual plots of both models");
  card(s, 8.3, 3.1, 4.4, 3.8, "bias card");
  s.addText([
    { text: "Over or under?", options: { bold: true, fontSize: 16, breakLine: true } },
    { text: "Simple: 94 days over, 106 under; errors up to about 10 °C.", options: { breakLine: true } },
    { text: "Multiple: 103 days over, 97 under; errors within about 4 °C. Mean residual −0.04 °C, so no overall bias.", options: { breakLine: true } },
    { text: "Hot days (> 30 °C) are slightly under-estimated (+0.32 °C)." },
  ], { x: 8.5, y: 3.2, w: 4.0, h: 3.6, fontSize: 14, color: C.text1, valign: "middle", margin: 0, isTextBox: true, paraSpaceAfter: 6, objectName: "bias text" });
  s.addNotes("This slide compares both models side by side on 200 unseen days. MAE is the average absolute error, MSE squares the errors, RMSE brings that back to degrees, and R squared is the share of variation explained. The multiple model cuts the typical error from about 3.3 degrees to under 1 degree and explains 94 percent of the variation against 28 percent for the simple model. Residuals are actual minus predicted. Both models are balanced overall, but the simple model makes errors up to 10 degrees while the multiple model stays within about 4. The multiple model is slightly too low on the hottest days.");

  // ===== 15. Conclusion =====
  pres.addSection({ title: "Conclusion" });
  s = pres.addSlide({ masterName: "CONTENT_DARK", sectionTitle: "Conclusion" });
  s.addText("Key findings", { placeholder: "title" });
  const kf = [
    ["Temperature is predictable", "Five weather factors explain 93.9 % of temperature variation, typical error about 1 °C.", C.accent1],
    ["Yesterday matters most", "Previous-day temperature (r = 0.96) outweighs humidity (−0.56), pressure and sunshine.", C.accent2],
    ["Location matters", "Cities differ significantly (ANOVA p < 0.001); rainy and dry days do not (p = 0.097).", C.accent3],
    ["Honest, unbiased model", "Residuals centre on zero; hot days are slightly under-estimated.", C.accent5],
  ];
  kf.forEach((k, i) => {
    const x = 0.6 + (i % 2) * 6.15, y = 1.6 + Math.floor(i / 2) * 2.35;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 5.95, h: 2.15, rectRadius: 0.12, fill: { color: "2A3160" }, line: { type: "none" }, objectName: "finding card " + (i + 1) });
    badge(s, x + 0.3, y + 0.3, i + 1, k[2], "finding badge " + (i + 1));
    s.addText(k[0], { x: x + 1.0, y: y + 0.3, w: 4.7, h: 0.5, fontSize: 20, bold: true, color: C.background1, margin: 0, valign: "middle", isTextBox: true, objectName: "finding title " + (i + 1) });
    s.addText(k[1], { x: x + 1.0, y: y + 0.9, w: 4.7, h: 1.1, fontSize: 14, color: C.background2, margin: 0, valign: "top", isTextBox: true, objectName: "finding text " + (i + 1) });
  });
  s.addText("Next steps: use real IMD weather records, add more years, and try non-linear models such as random forests.", { x: 0.6, y: 6.35, w: 12.1, h: 0.5, fontSize: 16, italic: true, color: "B9C0DC", margin: 0, isTextBox: true, objectName: "next steps" });
  s.addNotes("To summarise: temperature can be predicted well from a handful of weather variables, previous-day temperature is the dominant predictor, location matters but rain on the day does not significantly change temperature, and the model is unbiased. A natural extension is to replace the synthetic data with real records from the India Meteorological Department and try non-linear models.");

  await pres.writeFile({ fileName: FILE });
  await applyTheme(FILE, THEME);
  console.log("Presentation created:", FILE);
})();
