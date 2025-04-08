import pytest
import pandas as pd
from src.data_processing import load_data, process_data

def test_load_data():
    # Test loading data from the CSV file
    data = load_data('data/GlobalLandTemperaturesByCountry.csv')
    assert isinstance(data, pd.DataFrame), "Loaded data should be a DataFrame"
    assert not data.empty, "Loaded data should not be empty"
    assert 'Country' in data.columns, "Data should contain 'Country' column"
    assert 'AverageTemperature' in data.columns, "Data should contain 'AverageTemperature' column"

def test_process_data():
    # Test processing of data
    sample_data = pd.DataFrame({
        'Country': ['India', 'India', 'India'],
        'AverageTemperature': [25.0, None, 27.0],
        'dt': pd.to_datetime(['2000-01-01', '2001-01-01', '2002-01-01'])
    })
    processed_data = process_data(sample_data)
    
    # Check if missing values are handled
    assert processed_data['AverageTemperature'].isnull().sum() == 0, "Missing values should be interpolated"
    assert len(processed_data) == 3, "Processed data should have the same number of rows"
    assert processed_data['AverageTemperature'].iloc[1] == 26.0, "Interpolated value should be correct"