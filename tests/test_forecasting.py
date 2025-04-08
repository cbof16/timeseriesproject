import pytest
import pandas as pd
from src.forecasting import forecast_temperature

def test_forecast_temperature():
    # Sample input data for testing
    sample_data = {
        'dt': pd.date_range(start='2000-01-01', periods=10, freq='Y'),
        'AverageTemperature': [25.0, 25.5, 26.0, 26.5, 27.0, 27.5, 28.0, 28.5, 29.0, 29.5]
    }
    df = pd.DataFrame(sample_data)
    df.set_index('dt', inplace=True)

    # Call the forecasting function
    forecasted_values = forecast_temperature(df)

    # Check if the output is as expected
    assert len(forecasted_values) == 5  # Assuming we forecast 5 years ahead
    assert all(isinstance(value, float) for value in forecasted_values)  # Ensure all values are floats

def test_forecast_temperature_empty_data():
    # Test with empty DataFrame
    empty_df = pd.DataFrame(columns=['dt', 'AverageTemperature'])
    
    # Call the forecasting function and expect it to raise a ValueError
    with pytest.raises(ValueError, match="No data available for forecasting"):
        forecast_temperature(empty_df)

def test_forecast_temperature_invalid_data():
    # Test with invalid data (non-numeric)
    invalid_data = {
        'dt': pd.date_range(start='2000-01-01', periods=10, freq='Y'),
        'AverageTemperature': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    }
    df = pd.DataFrame(invalid_data)
    df.set_index('dt', inplace=True)

    # Call the forecasting function and expect it to raise a TypeError
    with pytest.raises(TypeError, match="could not convert string to float"):
        forecast_temperature(df)

def test_arima_forecast():
    forecast_df, metrics = predict_future_temperatures(mock_data, years=5, model_type='arima')
    assert len(forecast_df[forecast_df['Type'] == 'Forecast']) == 5
    assert 'RMSE' in metrics

def test_exp_smoothing_forecast():
    forecast_df, metrics = predict_future_temperatures(mock_data, years=5, model_type='exp_smoothing')
    assert len(forecast_df[forecast_df['Type'] == 'Forecast']) == 5
    assert 'MAE' in metrics