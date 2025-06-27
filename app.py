from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# OpenWeatherMap API key (you'll need to get this from OpenWeatherMap)
API_KEY = os.getenv('9b01646bb0e019992db214aecdf67223')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.json.get('city')
    
    if not city:
        return jsonify({'error': 'City name is required'}), 400
    
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            weather_data = {
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'city': data['name'],
                'country': data['sys']['country']
            }
            return jsonify(weather_data)
        else:
            return jsonify({'error': 'City not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
