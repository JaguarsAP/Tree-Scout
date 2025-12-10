# Tree-Scout: U.S. County-Level Deforestation Forecasting (2010–2026)

## 🚀 Overview

Tree-Scout is a full end-to-end machine learning pipeline designed to **monitor, analyze, and forecast U.S. county-level forest loss** using environmental, economic, and spatial data. Using data from Global Forest Watch, NOAA, OWID, Yahoo Finance, and U.S. Census, the project builds a unified dataset covering climate indicators, economic logging signals, county geospatial boundaries, and historical deforestation trends.

We construct a rich feature set with over **45 engineered variables**, train a **Random Forest regression model**, and generate **multi-year forecasts** (2021–2026). These predictions are visualized through **interactive maps**, including a slider animation and a 2026 risk heatmap.

This README serves as both the **project report** and **reproduction guide**, per the requirements.

---

## 📦 How to Build & Run (Required)

### **Installation**

```bash
make install
```

This installs all required Python dependencies.

### **Run the Project**

```bash
make run
```

This executes the main notebook or script containing:

* Data merging
* Feature engineering
* Model training
* Recursive forecasting
* Map generation

### **Run Tests (with GitHub Actions CI)**

```bash
make test
```

This runs a minimal suite of automated tests to verify core functionality.

---

## 📂 Project Structure

```
project/
│── data/
│   ├── county_forest_data_enhanced.csv
│   ├── US_County_Boundingboxes.csv
│── src/
│   ├── features.py
│   ├── model.py
│   ├── visualize.py
│── tests/
│   ├── test_features.py
│   ├── test_model.py
│── notebook/
│   ├── tree-cover-prediction.ipynb
│── Makefile
│── README.md
│── requirements.txt
```

---

## 🌲 Project Description

Tree-Scout is a machine learning system designed to **analyze and forecast deforestation across all U.S. counties** using historical data, climate trends, economic indicators, and spatial information. The project draws from multiple real-world datasets, including:

* Global Forest Watch (Tree cover loss)
* NOAA (CO₂ and climate data)
* Our World in Data (National emissions trends)
* Yahoo Finance (Logging sector stock indices)
* U.S. Census TIGER/Line datasets (County shapefiles & centroids)

We merge, clean, and engineer these datasets into a unified analytical table. Feature engineering includes:

* Lagged variables (lag-1, 3-year rolling means)
* Polynomial interactions between CO₂ and logging trends
* Percent changes and time-based derivatives
* Geospatial features (centroid latitude/longitude)
* Stock index behavior for major logging companies

A **Random Forest regression model** is trained using a temporally appropriate split:

* **Train:** 2010–2017
* **Validation:** 2018–2019
* **Test:** 2020

This ensures no information leakage from future years.

The final model is then used for **recursive forecasting**, predicting annual tree cover loss for **2021–2026**. These years are plotted on animated maps and risk heatmaps.

---

## ⚙️ Data Processing & Feature Engineering

### Key Steps

1. **Merge all datasets** into a unified frame keyed by FIPS + Year.
2. **Clean missing or inconsistent values**, standardize column formats.
3. **Engineer 45+ features**, including:

   * Climate trend features
   * Logging economic indicators
   * Lagged forest loss
   * Polynomial interactions (degree 2)
   * Rolling averages, percent changes
4. **Geospatial preprocessing** using bounding box data and centroids.
5. **Train/validation/test temporal split** for proper forecasting.

### Example Engineered Features

* `Tree_Loss_Hectares_lag1`
* `CO2_Per_Capita_t_x^2`
* `Logging_Index_Avg_Price_x_pct_chg`
* `Carbon_Emissions_Mg_CO2e_ma3`

---

## 🤖 Model Training

We use a **Random Forest Regressor** with these hyperparameters:

```python
RandomForestRegressor(
    n_estimators=300,
    max_depth=12,
    min_samples_split=5,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)
```

### Why Random Forest?

* Handles non-linear ecological relationships
* Robust to missing/erratic county-year data
* Captures interactions among climate, economic, and geographic variables

---

## 📈 Model Evaluation

We report metrics on **training**, **validation**, and **test** years.

### Metrics Computed

* **R² Score**
* **RMSE** (Root Mean Squared Error)
* **MAE** (Mean Absolute Error)
* **MAPE** (Mean Absolute Percentage Error)

### Interpretation Summary

* Strong performance on the 2020 test year
* Moderate drop on validation years (2018–2019) due to major wildfire anomalies
* Strong training fit without excessive overfitting
* Predictive behavior is consistent with ecological and economic patterns

---

## 🔮 Recursive Forecasting (2021–2026)

To predict future years, we use **recursive time-series forecasting**:

1. Predict 2021 using 2020 + lag features
2. Merge predictions into dataset
3. Recompute lag & rolling features
4. Predict 2022 using updated dataset
5. Repeat until 2026

This creates a fully synthetic but structurally coherent forecast.

---

## 🗺️ Visualizations

Tree-Scout includes several interactive Plotly maps.

### **1. U.S. County Map Slider (2010–2026)**

* Points represent counties
* Color = log-scaled tree cover loss
* Slider lets user explore by year

### **2. 2026 Risk Heatmap**

Counties are bucketed into:

* **Low Risk**
* **Medium Risk**
* **High Risk**
* **Extreme Risk**

Based on predicted 2026 deforestation.

### **3. Additional Plots**

* Feature importance bar chart
* Predicted vs. actual scatterplots
* Residual diagnostics

---

## 🧪 Testing Framework

Minimal unit tests ensure the pipeline is functioning correctly:

* Feature engineering adds expected columns
* Model trains without crashing
* Forecasting loop outputs correct number of future years
* Visualization functions return Plotly figures

GitHub Actions runs these tests automatically.

---

## 🚧 Future Work

* Integrate fire risk & drought severity indices
* Add satellite NDVI/land-cover time series
* Fit gradient boosting or temporal deep learning models
* Deploy as an interactive dashboard (Streamlit or Flask)

---

## 👥 Contributors

* Alexander Pfau
* Anthony Hardimon

---


