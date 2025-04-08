import pandas as pd

def load_data(file_path):
    """
    Load the temperature data from a CSV file.
    
    Parameters:
    - file_path: str, path to the CSV file
    
    Returns:
    - DataFrame containing the temperature data
    """
    data = pd.read_csv(file_path)
    data['dt'] = pd.to_datetime(data['dt'])
    return data

def preprocess_data(data, country):
    """
    Preprocess the temperature data for a specific country.
    
    Parameters:
    - data: DataFrame, raw temperature data
    - country: str, name of the country to filter data for
    
    Returns:
    - DataFrame containing the processed temperature data for the specified country
    """
    country_data = data[data['Country'] == country].copy()
    
    if country_data.empty:
        raise ValueError(f"No data found for country: {country}")
    
    # Handle missing values with time-based interpolation
    temperature_data = country_data['AverageTemperature'].interpolate(method='time')
    
    # Resample yearly for better visualization
    yearly_avg_temp = temperature_data.resample('Y').mean()
    
    # Remove years with NaN values after resampling
    yearly_avg_temp = yearly_avg_temp.dropna()
    
    return yearly_avg_temp

def get_country_temperature_data(file_path, country):
    """
    Load and preprocess temperature data for a specific country.
    
    Parameters:
    - file_path: str, path to the CSV file
    - country: str, name of the country to filter data for
    
    Returns:
    - DataFrame containing the processed temperature data for the specified country
    """
    data = load_data(file_path)
    return preprocess_data(data, country)

def get_country_data(data, country):
    """
    Filter data for a specific country.
    
    Parameters:
    - data: DataFrame, raw temperature data
    - country: str, name of the country to filter data for
    
    Returns:
    - DataFrame containing the filtered data for the specified country
    """
    country_data = data[data['Country'] == country].copy()
    if country_data.empty:
        raise ValueError(f"No data found for country: {country}")
    country_data['AverageTemperature'] = country_data['AverageTemperature'].interpolate(method='time')
    return country_data

def get_available_countries(data):
    """
    Get a list of all available countries in the dataset.
    
    Parameters:
    - data: DataFrame, raw temperature data
    
    Returns:
    - List of unique country names
    """
    return sorted(data['Country'].unique())