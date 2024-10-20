import requests
import schedule
import time
import sqlite3
from datetime import datetime

import matplotlib.pyplot as plt
import seaborn as sns

# Your API key from OpenWeatherMap
API_KEY = "aeeda406e29a6790207318d04e6a90b9"

cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad","Pune"]


conn = sqlite3.connect('weather_data.db')
c = conn.cursor()

# Create a table for storing weather data
c.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        temperature REAL,
        feels_like REAL,
        weather TEXT,
        timestamp INTEGER
    )
''')

def store_weather_data(city, temp, feels_like, weather, timestamp):
    c.execute('''
        INSERT INTO weather (city, temperature, feels_like, weather, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (city, temp, feels_like, weather, timestamp))
    conn.commit()



def calculate_daily_summary():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()

    # Query weather data grouped by day
    c.execute('''
        SELECT city, 
               DATE(timestamp, 'unixepoch') as day, 
               AVG(temperature) as avg_temp, 
               MAX(temperature) as max_temp, 
               MIN(temperature) as min_temp,
               weather
        FROM weather
        GROUP BY city, day
    ''')
    
    results = c.fetchall()

    print("\nDaily Weather Summaries:")
    for row in results:
        city, day, avg_temp, max_temp, min_temp, weather = row
        print(f"{day} - {city} | Avg Temp: {avg_temp:.2f}°C, Max Temp: {max_temp:.2f}°C, Min Temp: {min_temp:.2f}°C, Weather: {weather}")

    conn.close()

# Call the function to generate summaries
calculate_daily_summary()

# Define alert thresholds
ALERT_TEMP_THRESHOLD = 35.0  # User-defined threshold for high temperature alerts
ALERT_CONSECUTIVE_THRESHOLD = 2  # Number of consecutive readings to trigger alert

def check_alerts():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()

    # Query the latest weather updates
    c.execute('''
        SELECT city, temperature, weather, timestamp 
        FROM weather
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (ALERT_CONSECUTIVE_THRESHOLD,))

    recent_readings = c.fetchall()

    alert_triggered = False
    if len(recent_readings) >= ALERT_CONSECUTIVE_THRESHOLD:
        # Check if temperature exceeds threshold for consecutive updates
        temp_exceeded = all(row[1] > ALERT_TEMP_THRESHOLD for row in recent_readings)
        
        if temp_exceeded:
            city = recent_readings[0][0]
            last_temp = recent_readings[0][1]
            last_weather = recent_readings[0][2]
            last_timestamp = datetime.utcfromtimestamp(recent_readings[0][3]).strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n[ALERT] High temperature alert for {city}!")
            print(f"Temperature exceeded {ALERT_TEMP_THRESHOLD}°C for {ALERT_CONSECUTIVE_THRESHOLD} consecutive readings.")
            print(f"Last reading: {last_temp:.2f}°C, Weather: {last_weather}, Time: {last_timestamp}")
            alert_triggered = True

    if not alert_triggered:
        print("\nNo alerts triggered at this time.")
    
    conn.close()

# Call the function to check for alerts
check_alerts()


def calculate_dominant_weather():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()

    # Query weather data grouped by day and city
    c.execute('''
        SELECT city, DATE(timestamp, 'unixepoch') as day, weather, COUNT(*) as weather_count
        FROM weather
        GROUP BY city, day, weather
        ORDER BY weather_count DESC
    ''')

    results = c.fetchall()

    print("\nDominant Weather Conditions:")
    for row in results:
        city, day, weather, count = row
        print(f"{day} - {city} | Dominant Weather: {weather} (Occurred {count} times)")

    conn.close()

# Call the function to calculate dominant weather
calculate_dominant_weather()



# Function to get weather data for a city
def get_weather(city_name):
    # API URL with city name and API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"

    # Make a request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract relevant information from the data
        temp_kelvin = data['main']['temp']
        weather_main = data['weather'][0]['main']
        feels_like_kelvin = data['main']['feels_like']
        timestamp = data['dt']
        
        # Convert temperatures from Kelvin to Celsius
        temp_celsius = temp_kelvin - 273.15
        feels_like_celsius = feels_like_kelvin - 273.15
        
        # Print the data
        print(f"City: {city_name}")
        print(f"Temperature: {temp_celsius:.2f} °C")
        print(f"Feels Like: {feels_like_celsius:.2f} °C")
        print(f"Weather: {weather_main}")
        print(f"Timestamp: {timestamp}")
    else:
        print(f"Failed to get data for {city_name}. Error code: {response.status_code}")

# # Test the function
# get_weather("Delhi")

def get_weather_cities(cities):
    weather_city=[]

    for city in cities:
        data= get_weather(city)
        if data:
            weather_city.append(data)
    return weather_city


# weather_data= get_weather_cities(cities)

# for data in weather_data:
#     print(f"{data['city']} - Temp: {data['temperature']:.2f}°C, Weather: {data['weather']}")

def schedule_weather_fetch():
    print("Fetching the data....")

    get_weather_cities(cities)
schedule.every(2).minutes.do(schedule_weather_fetch)

while True:
    schedule.run_pending()
    time.sleep(1)



