import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import linregress

def plot_temperature_trends(country_data, country):
    """
    Plot temperature trends for a country
    
    Args:
        country_data: DataFrame with country-specific data
        country: Name of the country (for title)
        
    Returns:
        Matplotlib figure
    """
    # Resample to yearly averages
    yearly_avg_temp = country_data['AverageTemperature'].resample('Y').mean().dropna()
    
    # Compute Moving Average (10-year)
    rolling_avg = yearly_avg_temp.rolling(window=10, min_periods=1).mean()
    
    # Fit a Linear Regression Trend Line
    years_since_start = np.arange(len(yearly_avg_temp))
    slope, intercept, _, _, _ = linregress(years_since_start, yearly_avg_temp.values)
    trend_line = intercept + slope * years_since_start
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # Plot data
    ax.plot(yearly_avg_temp, label=f"{country}'s Yearly Average", color='blue', alpha=0.6)
    ax.plot(rolling_avg, label="10-Year Moving Average", color='red', linewidth=2)
    ax.plot(yearly_avg_temp.index, trend_line, '--', color='green', 
           label=f"Trend Line ({slope:.3f}°C/year)")
    
    # Customize plot
    ax.set_title(f"Temperature Trends Over Time ({country})", fontsize=14, pad=20)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Temperature (°C)", fontsize=12)
    ax.legend(fontsize=10)
    
    # Rotate x-axis labels for readability
    plt.xticks(rotation=45, ha='right')
    
    # Adjust layout
    plt.tight_layout()
    
    return fig

def save_plot(filename):
    plt.savefig(filename, dpi=300)

def show_plot():
    plt.show()