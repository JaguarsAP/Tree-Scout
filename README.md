# Tree-Scout 🌲
**CS506 Final Project - Boston University**

Predicting U.S. county-level deforestation using machine learning with climate, economic, and satellite data.

## How to Build and Run

### Prerequisites
- Python 3.9+
- **No API key required!** Pre-cached data is included in the repository. If you would like to edit the years the model trains/predicts on, you will need a GFW api key.

### Installation

```bash
# Clone the repository
git clone https://github.com/JaguarsAP/Tree-Scout.git
cd Tree-Scout

# Install dependencies using Makefile
make install

# Or install manually
pip install notebook ipywidgets yfinance requests pandas numpy matplotlib seaborn plotly scikit-learn python-dotenv pytest
```

### Running the Notebook

```bash
make run
# Or manually:
jupyter notebook tree-cover-prediction.ipynb
```

> **Note for TAs/Instructors**: The notebook uses **pre-cached data files** (`county_forest_loss_data.csv`, `county_forest_data_enhanced.csv`) included in the repository. You can run the entire notebook without any API keys. The external data sources (NOAA, Our World in Data, Yahoo Finance) are all free and don't require authentication.

### Optional: Fetching Fresh Data

If you want to fetch fresh data from the Global Forest Watch API (not required):

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your GFW API key
# GFW_API_KEY=your_api_key_here

# Delete cached file to force re-fetch
rm county_forest_loss_data.csv
```

---

## Testing

### Running Tests

```bash
# Run all tests
make test

# Or manually:
pytest tests/ -v
```

### Test Coverage

Our test suite (`tests/test_api_and_data.py`) validates:

| Test Category | Description |
|--------------|-------------|
| **Data Format Validation** | Ensures `US_County_Boundingboxes.csv` has required columns (FIPS codes, coordinates) and valid coordinate ranges for continental US |
| **API Connectivity** | Verifies NOAA CO2 endpoint, Our World in Data emissions endpoint, and GFW API are accessible |
| **Forest Data Output** | Validates generated `county_forest_loss_data.csv` has correct columns, year ranges, and non-negative values |
| **Enhanced Data Features** | Checks that climate features (CO2, emissions) and stock price features are present in enhanced dataset |
| **Train/Test Split Integrity** | Ensures no temporal data leakage between training and test sets |

### GitHub Actions CI/CD

Tests run automatically on every push and pull request via `.github/workflows/tests.yml`.

[![Tests](https://github.com/JaguarsAP/Tree-Scout/actions/workflows/tests.yml/badge.svg)](https://github.com/JaguarsAP/Tree-Scout/actions/workflows/tests.yml)

---

## Data Processing Pipeline

### 1. Data Sources

| Source | Data | Purpose |
|--------|------|---------|
| **Global Forest Watch API** | Tree cover loss (hectares), Carbon emissions (Mg CO2e), Tree cover extent | Primary deforestation metrics per county |
| **NOAA Mauna Loa Observatory** | Atmospheric CO2 concentration (ppm) | Global climate indicator |
| **Our World in Data** | U.S. emissions (total, per capita, cumulative), Methane, Nitrous oxide | National emissions context |
| **Yahoo Finance** | Stock prices for Weyerhaeuser, Rayonier, PotlatchDeltic, Louisiana-Pacific | Logging industry economic indicators |
| **US Census** | County bounding boxes (FIPS codes, lat/lon coordinates) | Geographic reference for API queries |

### 2. Data Collection

The notebook fetches data for **3,000+ U.S. counties** using:
- **Parallel API requests** with `ThreadPoolExecutor` (10 workers)
- **Rate limiting** (30 requests/second) to respect API limits
- **Bounding box queries** converting county coordinates to GFW polygon format

### 3. Feature Engineering

We create **45+ features** across several categories:

#### Time Series Features
- **Lag features**: Previous 1-2 years of tree loss per county
- **Moving averages**: 3-year and 5-year rolling averages
- **Momentum indicators**: Percent change, acceleration (2nd derivative), volatility

#### Climate & Economic Features
- **Polynomial features** (degree 2): Interactions between CO2, emissions, tree loss, and stock prices
- **Climate lag features**: Lagged CO2/emissions with 3-year moving averages
- **Logging stock index**: Composite average of major timber company stock prices

#### Spatial Features
- **Area normalization**: Tree loss per km² to account for county size differences
- **Spatial clustering**: K-means clustering (10 regions) based on county centroids
- **Neighbor features**: Mean tree loss of counties in same spatial cluster

#### Calendar Features
- Year index, decade indicator, post-2014 policy flag

### 4. Data Merging & Output

The pipeline produces:

| Output File | Description |
|-------------|-------------|
| `county_forest_loss_data.csv` | Raw GFW data (tree loss, carbon emissions, tree cover extent) |
| `county_forest_data_enhanced.csv` | Merged dataset with all external features + polynomial terms |
| `county_forest_data_train.csv` | Training set (temporal split: ~70% of years) |
| `county_forest_data_test.csv` | Test set (temporal split: ~15% of years) |

---

## Description

I'm working with 1 partner, Anthony Hardimon. Together, we are monitoring the rate of deforestation in the U.S. to predict which counties are most likely to experience tree cover loss.

## Data

We use data from the **Global Forest Watch (GFW)** API, which tracks deforestation statistics including:
- Tree cover loss (annual hectares lost)
- Tree cover gain (annual hectares gained)  
- Primary forest loss (GLAD-S2 alerts)
- Deforestation hotspots (daily confidence-scored alerts)
- Cumulative forest change (loss − gain over multi-year spans)

We predict tree cover loss since 2010 for loss with >10% canopy capacity.

## Modeling

We use a **Random Forest Regressor** with:
- 300 estimators, max depth 12
- Temporal train/validation/test split to prevent data leakage
- Feature importance analysis to identify key predictors

## Visualization

Interactive visualizations built with **Plotly**:
- County-level tree loss maps with year slider animation
- Correlation heatmaps for climate and stock features
- Time series comparisons of CO2, tree loss, and logging stocks

## Testing Strategy

We use a **temporal train/test split**:
- Training: 2010-2017 (~70% of data)
- Validation: 2018-2019 (~15%)
- Test: 2020 (~15%)

This ensures the model is evaluated on future years it hasn't seen, simulating real-world prediction.

![Midterm Video](https://youtu.be/Nrnz_eqOdqE)


  
