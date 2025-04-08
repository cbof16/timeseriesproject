# Temperature Forecasting Application

A web application for analyzing historical temperature data and predicting future temperature trends up to 2050 using machine learning models.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Models](#models)
  - [Machine Learning Architecture](#machine-learning-architecture)
  - [Time Series Processing](#time-series-processing)
  - [Model Evaluation](#model-evaluation)
- [Contributing](#contributing)
- [License](#license)

## Overview

This application provides a user-friendly interface for analyzing historical temperature data and generating future temperature predictions. It uses machine learning models to forecast temperature trends from 2025 to 2050, helping users understand potential climate changes.

## Architecture

The application follows a modular architecture with the following components:

```
┌─────────────────────────────────────────────────────────────────────┐
│                          User Interface                             │
│                                                                     │
│  ┌─────────────┐                                ┌───────────────┐   │
│  │  Web Browser │ ◄───── HTTP/HTTPS ─────────► │  Flask Routes  │   │
│  └─────────────┘                                └───────────────┘   │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Application Core                            │
│                                                                     │
│  ┌─────────────┐     ┌─────────────┐     ┌───────────────────────┐  │
│  │Data Processor│ ◄► │  Forecaster  │ ◄► │ Visualization Engine  │  │
│  └─────────────┘     └─────────────┘     └───────────────────────┘  │
│         ▲                    ▲                       ▲              │
└─────────┼────────────────────┼───────────────────────┼──────────────┘
          │                    │                       │
          ▼                    ▼                       ▼
┌──────────────┐    ┌────────────────────┐    ┌────────────────────┐
│ Temperature  │    │  Machine Learning  │    │  Matplotlib/       │
│ Data (CSV)   │    │  Models            │    │  Visualization     │
└──────────────┘    └────────────────────┘    └────────────────────┘
```

### Backend
- **Flask**: Web framework for handling HTTP requests and serving the application
- **Gunicorn**: WSGI server for production deployment
- **Data Processing**: Pandas for data manipulation and analysis
- **Machine Learning**: 
  - Linear Regression for trend analysis
  - Exponential Smoothing for time series forecasting

### Frontend
- **HTML/CSS**: For the user interface
- **Bootstrap**: For responsive design
- **Matplotlib**: For data visualization

### Data Flow
1. User selects a country and model type
2. Backend loads and processes historical temperature data
3. Selected model generates predictions
4. Results are visualized and displayed to the user

## Features

- Country-specific temperature analysis
- Multiple forecasting models:
  - Linear Regression
  - Exponential Smoothing
- Interactive visualizations
- Confidence intervals for predictions
- Historical data comparison
- Export functionality for forecasts
- Responsive design

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd temperature-forecasting
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Development Mode
1. Start the Flask development server:
```bash
python src/ui/app.py
```

2. Access the application at `http://localhost:5000`

### Production Deployment
1. Make the deployment script executable:
```bash
chmod +x deploy.sh
```

2. Run the deployment script:
```bash
./deploy.sh
```

3. Access the application at `http://your-server:8000`

## Project Structure

```
temperature-forecasting/
├── data/
│   └── GlobalLandTemperaturesByCountry.csv
├── src/
│   ├── data_processing.py
│   ├── forecasting.py
│   ├── visualization.py
│   └── ui/
│       └── app.py
├── templates/
│   ├── index.html
│   └── results.html
├── static/
│   └── css/
│       └── style.css
├── requirements.txt
├── deploy.sh
└── README.md
```

## Models

### Machine Learning Architecture

This application implements a comprehensive time series forecasting architecture designed specifically for temperature data:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                       Time Series Forecasting Pipeline                       │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
         ┌────────────────────────────┼────────────────────────┐
         │                            │                        │
         ▼                            ▼                        ▼
┌──────────────────┐        ┌──────────────────┐      ┌──────────────────┐
│   Data Loading   │        │ Data Processing  │      │ Feature          │
│   & Validation   │───────►│ & Transformation │─────►│ Engineering      │
└──────────────────┘        └──────────────────┘      └──────────────────┘
                                                               │
         ┌────────────────┬────────────────┬─────────────────┐
         │                │                │                 │
         ▼                ▼                ▼                 ▼
┌──────────────┐  ┌─────────────┐  ┌────────────────┐ ┌─────────────────┐
│    Linear    │  │ Exponential │  │     Model      │ │   Confidence    │
│  Regression  │  │  Smoothing  │  │  Evaluation &  │ │   Interval      │
│   Forecasts  │  │  Forecasts  │  │   Selection    │ │   Generation    │
└──────────────┘  └─────────────┘  └────────────────┘ └─────────────────┘
         │                │                │                 │
         └────────────────┴────────────────┼─────────────────┘
                                           │
                                           ▼
                             ┌────────────────────────────┐
                             │    Forecast Visualization  │
                             │    & Result Presentation   │
                             └────────────────────────────┘
```

### Time Series Processing

The application employs a sophisticated approach to handling time series data:

#### 1. Data Preprocessing
- **Missing Value Handling**: 
  - Linear interpolation for short gaps
  - Seasonal decomposition for larger gaps
  - Rolling window techniques for outlier detection

- **Time Series Decomposition**:
  - Trend component extraction
  - Seasonal pattern identification
  - Residual noise analysis

- **Data Transformation**:
  - Moving averages (7-day, 30-day, annual) to smooth noisy data
  - Logarithmic transformations for stabilizing variance
  - Differencing for stationarity requirements

#### 2. Model Implementation

##### Linear Regression Model
```python
# Simplified implementation
from sklearn.linear_model import LinearRegression
import numpy as np

def linear_regression_forecast(historical_data, forecast_horizon):
    # Create features (time index)
    X = np.array(range(len(historical_data))).reshape(-1, 1)
    y = historical_data
    
    # Train model
    model = LinearRegression().fit(X, y)
    
    # Generate future time indices
    future_X = np.array(range(len(historical_data), 
                             len(historical_data) + forecast_horizon)).reshape(-1, 1)
    
    # Predict future values
    forecast = model.predict(future_X)
    
    # Calculate confidence intervals
    # [Implementation details for confidence intervals]
    
    return forecast, confidence_intervals
```

##### Exponential Smoothing
```python
# Simplified implementation
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def exponential_smoothing_forecast(historical_data, forecast_horizon):
    # Configure model with trend and seasonal components
    model = ExponentialSmoothing(
        historical_data,
        trend='add',          # Additive trend component
        seasonal='add',       # Additive seasonal component
        seasonal_periods=12   # Monthly seasonality
    )
    
    # Fit the model
    fitted_model = model.fit(optimized=True)
    
    # Generate forecasts with confidence intervals
    forecasts = fitted_model.forecast(forecast_horizon)
    conf_int = fitted_model.get_prediction(
        start=len(historical_data),
        end=len(historical_data) + forecast_horizon - 1
    ).conf_int(alpha=0.05)  # 95% confidence intervals
    
    return forecasts, conf_int
```

### Model Evaluation

The forecasting models are evaluated using multiple metrics to ensure accuracy:

| Metric | Description | Implementation |
|--------|-------------|----------------|
| RMSE | Root Mean Squared Error | `sqrt(mean_squared_error(actual, predicted))` |
| MAE | Mean Absolute Error | `mean_absolute_error(actual, predicted)` |
| MAPE | Mean Absolute Percentage Error | `mean(abs((actual - predicted) / actual) * 100)` |
| AIC | Akaike Information Criterion | Model-specific implementation |
| BIC | Bayesian Information Criterion | Model-specific implementation |

#### Cross-Validation Strategy

For time series validation, we implement a time series cross-validation approach:

```
Training data          Test data
[------------------]  [--------]  Fold 1
[----------------------]  [--------]  Fold 2
[----------------------------]  [--------]  Fold 3
```

This expanding window approach ensures that:
1. Temporal dependencies are preserved
2. All available historical data is used
3. Model performance is tested on multiple future periods

### Prediction Confidence Intervals

For each forecast, the application generates:
- Point estimates (expected temperature)
- 95% confidence intervals
- Prediction intervals accounting for:
  - Model parameter uncertainty
  - Random variation in future values
  - Seasonal effects

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Temperature data source: [Global Historical Climatology Network](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/global-historical-climatology-network-ghcn)
- Flask and Gunicorn for web framework and server
- Pandas and NumPy for data processing
- Matplotlib for visualization