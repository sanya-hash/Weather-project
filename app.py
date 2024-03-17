# # Import necessary libraries
# from flask import Flask, render_template
# from flask_socketio import SocketIO

# # Initialize Flask application
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'

# # Initialize Socket.IO instance
# socketio = SocketIO(app)

# # Route for serving HTML page
# @app.route('/')
# def index():
#     return render_template('index.html')

# # WebSocket connection event handler
# @socketio.on('connect')
# def handle_connect():
#     # TODO: Implement code for establishing a WebSocket connection with the client
#     pass

# # Background process for retrieving temperature data and emitting it to clients
# def emit_temperature_data():
#     # TODO: Implement code for retrieving temperature data from sensors
#     # TODO: Emit the temperature data to the connected clients using socketio.emit()

# # Run the Flask application with Socket.IO
#  if __name__ == '__main__':
#     socketio.start_background_task(emit_temperature_data)
#     socketio.run(app)


# # importing requests and json
# import requests, json
# # base URL
# BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
# CITY = "Hyderabad"
# # API key API_KEY = "Your API Key"
# # upadting the URL
# URL = BASE_URL + "q=" + CITY + "&appid=" + "37f710f3ede5ef84803f8d39eca46420"
# # HTTP request
# response = requests.get(URL)
# # checking the status code of the request
# if response.status_code == 200:
#    # getting data in the json format
#    data = response.json()
#    # getting the main dict block
#    main = data['main']
#    # getting temperature
#    temperature = main['temp']
#    # getting the humidity
#    humidity = main['humidity']
#    # getting the pressure
#    pressure = main['pressure']
#    # weather report
#    report = data['weather']
#    print(f"{CITY:-^30}")
#    print(f"Temperature: {temperature}")
#    print(f"Humidity: {humidity}")
#    print(f"Pressure: {pressure}")
#    print(f"Weather Report: {report[0]['description']}")
# else:
#    # showing the error message
#    print("Error in the HTTP request")



# from flask import Flask, render_template, request
# from flask_socketio import SocketIO, emit
# import requests

# app = Flask(__name__)
# socketio = SocketIO(app)

# def get_weather(city_name):
#     BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
#     API_KEY = "37f710f3ede5ef84803f8d39eca46420"
#     URL = f"{BASE_URL}q={city_name}&appid={API_KEY}"
#     response = requests.get(URL)
#     if response.status_code == 200:
#         data = response.json()
#         main = data['main']
#         temperature = main['temp']
#         humidity = main['humidity']
#         pressure = main['pressure']
#         weather_report = data['weather'][0]['description']
#         return {
#             "city": city_name,
#             "temperature": temperature,
#             "humidity": humidity,
#             "pressure": pressure,
#             "weather_report": weather_report
#         }
#     else:
#         return None

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/weather', methods=['POST'])
# def weather():
#     city_name = request.form['city']
#     weather_info = get_weather(city_name)
#     if weather_info:
#         return render_template('weather.html', weather=weather_info)
#     else:
#         return "Error fetching weather data."

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected')

# @socketio.on('get_temperature')
# def send_temperature(city):
#     weather_info = get_weather(city)
#     if weather_info:
#         emit('temperature_data', {
#             'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             'temperature': weather_info['temperature'],
#             'location': weather_info['city']
#         })

# if __name__ == '__main__':
#     socketio.run(app, debug=True)




from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
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
            'location': weather_info['city']
        })

if __name__ == '__main__':
    socketio.run(app, debug=True)
