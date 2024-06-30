from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

API_KEY = "d02bf30a9a75cd45985b33bb2889aebc"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    date_str = request.args.get('date')

    if not city or not date_str:
        return jsonify({"error": "Please provide both city and date parameters."}), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Date format should be YYYY-MM-DD."}), 400

    response = requests.get(BASE_URL, params={
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    })

    if response.status_code != 200:
        return jsonify({"error": "City not found or other error."}), response.status_code

    data = response.json()
    current_temp = data['main']['temp']
    min_temp = data['main']['temp_min']
    max_temp = data['main']['temp_max']
    humidity = data['main']['humidity']

    # Mock average calculation (using only current data for simplicity)
    avg_temp = (min_temp + max_temp) / 2

    weather_info = {
        "city": city,
        "date": date_str,
        "min_temp": min_temp,
        "max_temp": max_temp,
        "avg_temp": avg_temp,
        "humidity": humidity
    }

    return jsonify(weather_info)

app.run(debug=True)