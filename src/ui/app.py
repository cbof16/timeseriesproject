from flask import Flask, render_template, request, jsonify, send_file
import os
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

# Use relative imports for modules within the package
from ..data_processing import load_data, get_country_data, get_available_countries
from ..visualization import plot_temperature_trends
from ..forecasting import predict_future_temperatures

def create_app():
    app = Flask(__name__, 
                template_folder='../../templates',
                static_folder='../../static')
    
    # Load and process the temperature data
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                           'data', 'GlobalLandTemperaturesByCountry.csv')
    data = load_data(file_path)
    
    @app.route('/')
    def index():
        countries = get_available_countries(data)
        return render_template('index.html', countries=countries)
    
    @app.route('/analyze', methods=['POST'])
    def analyze():
        country = request.form.get('country')
        forecast_years = int(request.form.get('forecast_years', 10))
        model_type = request.form.get('model_type', 'linear')
        
        # Get country data
        country_data = get_country_data(data, country)
        
        # Generate visualization
        fig = plot_temperature_trends(country_data, country)
        
        # Save plot to memory
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        plot_data = base64.b64encode(buf.getbuffer()).decode('ascii')
        plt.close(fig)
        
        # Generate forecast
        forecast_df, metrics = predict_future_temperatures(country_data, years=forecast_years, model_type=model_type)
        
        # Prepare forecast data for display
        historical = forecast_df[forecast_df['Type'] == 'Historical'].tail(10)
        forecast = forecast_df[forecast_df['Type'] == 'Forecast']
        
        # Format dates for display
        historical['Year'] = historical['Date'].dt.year
        forecast['Year'] = forecast['Date'].dt.year
        
        return render_template('results.html', 
                             country=country,
                             plot_data=plot_data,
                             historical=historical.to_dict('records'),
                             forecast=forecast.to_dict('records'),
                             metrics=metrics,
                             model_type=model_type)
    
    @app.route('/download_forecast', methods=['POST'])
    def download_forecast():
        # Get forecast data from form
        forecast_data = json.loads(request.form.get('forecast_data'))
        country = request.form.get('country')
        
        # Convert to DataFrame
        df = pd.DataFrame(forecast_data)
        
        # Save to CSV
        csv_data = io.StringIO()
        df.to_csv(csv_data, index=False)
        csv_data.seek(0)
        
        # Create response
        return send_file(
            io.BytesIO(csv_data.getvalue().encode()),
            mimetype='text/csv',
            download_name=f'temperature_forecast_{country}.csv',
            as_attachment=True
        )
    
    return app

# For direct execution of app.py
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)