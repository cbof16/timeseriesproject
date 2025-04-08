import pandas as pd
import numpy as np
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class TemperatureForecaster:
    def __init__(self, data):
        self.data = data
        self.model = None

    def preprocess_data(self):
        # Handle missing values with time-based interpolation
        self.data['AverageTemperature'] = self.data['AverageTemperature'].interpolate(method='time')
        # Resample yearly for better analysis
        self.data = self.data.resample('Y').mean().dropna()

    def fit_model(self):
        years_since_start = np.arange(len(self.data))
        slope, intercept, _, _, _ = linregress(years_since_start, self.data['AverageTemperature'].values)
        self.model = (slope, intercept)

    def predict_future(self, years_ahead):
        if self.model is None:
            raise ValueError("Model has not been fitted yet.")
        slope, intercept = self.model
        future_years = np.arange(len(self.data), len(self.data) + years_ahead)
        predictions = intercept + slope * future_years
        return predictions

    def get_trend_slope(self):
        if self.model is None:
            raise ValueError("Model has not been fitted yet.")
        slope, _ = self.model
        return slope * 10  # Convert slope to °C per decade

def load_data(file_path):
    data = pd.read_csv(file_path)
    data['dt'] = pd.to_datetime(data['dt'])
    data.set_index('dt', inplace=True)
    return data

def filter_country_data(data, country):
    country_data = data[data['Country'] == country].copy()
    if country_data.empty:
        raise ValueError(f"No data found for country: {country}")
    return country_data[['AverageTemperature']]

def predict_future_temperatures(country_data, years=10, model_type='linear'):
    """
    Predict future temperatures based on historical data using different models.
    
    Args:
        country_data: DataFrame with country-specific data
        years: Number of years to forecast
        model_type: Type of forecasting model ('linear', 'arima', or 'exponential')
        
    Returns:
        Tuple of (DataFrame with forecasted temperatures, metrics dictionary)
    """
    # Get yearly averages
    yearly_avg_temp = country_data['AverageTemperature'].resample('Y').mean().dropna()
    
    # Create forecast dates
    last_date = yearly_avg_temp.index[-1]
    future_dates = pd.date_range(start=last_date, periods=years+1, freq='Y')[1:]
    
    # Metrics dictionary
    metrics = {}
    
    if model_type == 'linear':
        # Linear regression model
        X = np.arange(len(yearly_avg_temp)).reshape(-1, 1)
        y = yearly_avg_temp.values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Generate future X values
        future_X = np.arange(len(yearly_avg_temp), len(yearly_avg_temp) + years).reshape(-1, 1)
        predictions = model.predict(future_X)
        
        # Evaluate model
        train_predictions = model.predict(X)
        metrics = calculate_metrics(y, train_predictions)
    
    elif model_type == 'arima':
        # ARIMA model
        model = ARIMA(yearly_avg_temp.values, order=(1, 1, 1))
        model_fit = model.fit()
        
        # Forecast
        predictions = model_fit.forecast(steps=years)
        
        # Evaluate model
        train_predictions = model_fit.predict(start=1, end=len(yearly_avg_temp)-1)
        metrics = calculate_metrics(yearly_avg_temp.values[1:], train_predictions)
    
    elif model_type == 'exponential':
        # Exponential Smoothing model
        model = ExponentialSmoothing(yearly_avg_temp.values, trend='add', seasonal=None)
        model_fit = model.fit()
        
        # Forecast
        predictions = model_fit.forecast(years)
        
        # Evaluate model
        train_predictions = model_fit.fittedvalues
        metrics = calculate_metrics(yearly_avg_temp.values, train_predictions)
    
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Create forecast DataFrame
    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'Temperature': predictions,
        'Type': 'Forecast'
    })
    
    # Add historical data for reference
    historical_df = pd.DataFrame({
        'Date': yearly_avg_temp.index,
        'Temperature': yearly_avg_temp.values,
        'Type': 'Historical'
    })
    
    # Combine historical and forecast
    result_df = pd.concat([historical_df, forecast_df])
    
    return result_df, metrics

def calculate_metrics(actual, predicted):
    mse = mean_squared_error(actual, predicted)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(actual, predicted)
    return {'MSE': round(mse, 4), 'RMSE': round(rmse, 4), 'MAE': round(mae, 4)}