from flask import Blueprint, render_template, request
from src.forecasting import forecast_temperature

ui = Blueprint('ui', __name__)

@ui.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        country = request.form.get('country')
        year = request.form.get('year')
        if country and year:
            forecast = forecast_temperature(country, int(year))
            return render_template('results.html', forecast=forecast, country=country, year=year)
    return render_template('index.html')

def create_country_input_form():
    return '''
    <form method="POST">
        <label for="country">Country:</label>
        <input type="text" id="country" name="country" required>
        <label for="year">Year:</label>
        <input type="number" id="year" name="year" required>
        <button type="submit">Forecast Temperature</button>
    </form>
    '''