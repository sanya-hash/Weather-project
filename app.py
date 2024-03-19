from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bruh'  
socketio = SocketIO(app)

def kelvin_to_celsius(temperature_kelvin):
    temperature_celsius = temperature_kelvin - 273.15
    return round(temperature_celsius, 2)

def get_weather(city_name):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "37f710f3ede5ef84803f8d39eca46420"
    URL = f"{BASE_URL}q={city_name}&appid={API_KEY}"
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperature_kelvin = main['temp']
        temperature_celsius = kelvin_to_celsius(temperature_kelvin)
        humidity = main['humidity']
        pressure = main['pressure']
        weather_report = data['weather'][0]['description']
        return {
            "city": city_name,
            "temperature": temperature_celsius,
            "humidity": humidity,
            "pressure": pressure,
            "weather_report": weather_report
        }
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('get_temperature')
def send_temperature(data):
    city = data['city']
    weather_info = get_weather(city)
    if weather_info:
        emit('temperature_data', {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': weather_info['temperature'],
            'location': weather_info['city'],
            'humidity': weather_info['humidity'],
            'pressure': weather_info['pressure'],


        })

if __name__ == '__main__':
    socketio.run(app, debug=True)
