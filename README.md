# 🚲 Bike Rental Demand Prediction

A machine learning project to predict bike rental demand using weather, temporal, and seasonal features.

## 📋 Project Overview

This project analyzes the Capital Bikeshare dataset (2011-2012) to build predictive models for bike rental demand. Accurate predictions help optimize bike-sharing operations, improve resource allocation, and enhance customer satisfaction.

## 🎯 Key Features

- **Comprehensive EDA**: Visualizations of temporal patterns, weather impact, and correlations
- **Multiple Models**: Linear Regression, Ridge, Lasso, Decision Tree, Random Forest, Gradient Boosting, XGBoost
- **Cross-Validation**: 5-fold CV for robust model evaluation
- **Hyperparameter Tuning**: GridSearchCV for optimal model parameters
- **Feature Importance**: Analysis and visualization of key predictors

## 📁 Project Structure

```
PRCP-1018-BikeRental/
├── Data/
│   ├── Bike_Rental_Demand_Prediction_Datamites.ipynb  # Main analysis notebook
│   ├── hour.csv                                         # Hourly rental data
│   ├── day.csv                                          # Daily rental data
│   ├── Readme.txt                                       # Dataset documentation
│   └── bike sharing.docx                                # Additional documentation
├── requirements.txt                                     # Python dependencies
├── pyproject.toml                                       # UV project configuration
├── uv.lock                                              # Locked dependencies
└── README.md                                            # This file
```

## 🚀 Quick Start

### Using UV (Recommended)

```bash
# Clone the repository
cd PRCP-1018-BikeRental

# Create virtual environment and install dependencies
uv sync

# Activate the virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Start Jupyter Notebook
jupyter notebook Data/Bike_Rental_Demand_Prediction_Datamites.ipynb
```

### Using pip

```bash
# Create virtual environment
python -m venv .venv

# Activate
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start Jupyter
jupyter notebook Data/Bike_Rental_Demand_Prediction_Datamites.ipynb
```

## 📊 Dataset Information

| Feature | Description |
|---------|-------------|
| `instant` | Record index |
| `dteday` | Date |
| `season` | Season (1=Spring, 2=Summer, 3=Fall, 4=Winter) |
| `yr` | Year (0=2011, 1=2012) |
| `mnth` | Month (1-12) |
| `hr` | Hour (0-23) |
| `holiday` | Whether it's a holiday |
| `weekday` | Day of the week |
| `workingday` | 1 if neither weekend nor holiday |
| `weathersit` | Weather condition (1=Clear to 4=Heavy Rain) |
| `temp` | Normalized temperature |
| `atemp` | Normalized feeling temperature |
| `hum` | Normalized humidity |
| `windspeed` | Normalized wind speed |
| `cnt` | **Target** - Total bike rentals |

## 📈 Model Performance

| Model | MAE | RMSE | R² Score |
|-------|-----|------|----------|
| Random Forest | ~35 | ~55 | ~0.92 |
| XGBoost | ~34 | ~53 | ~0.93 |
| Gradient Boosting | ~38 | ~58 | ~0.91 |
| Ridge Regression | ~96 | ~130 | ~0.55 |
| Linear Regression | ~96 | ~130 | ~0.55 |

*Note: Actual values may vary based on random state and hyperparameters*

## 🔑 Key Insights

1. **Hour of day** is the most important feature - clear rush-hour patterns (8 AM, 5-6 PM)
2. **Temperature** positively correlates with rentals
3. **Weather conditions** significantly impact demand - clear weather boosts rentals
4. **Year 2012** shows higher rentals than 2011 (growing adoption)
5. **Summer and Fall** have higher demand than Spring and Winter

## 📜 License

See `Data/Readme.txt` for dataset citation requirements.

## 🙏 Acknowledgments

Dataset provided by Capital Bikeshare and UC Irvine Machine Learning Repository.
