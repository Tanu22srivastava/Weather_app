# Weather Monitoring and Alert System

## Overview

This project is a real-time weather monitoring and alert system that fetches weather data from the [OpenWeatherMap API](https://openweathermap.org/) and processes it to provide daily summaries, trigger alerts based on user-defined thresholds, and visualize trends. The system is designed to fetch weather data for six major cities in India (Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad).

## Features

- **Real-Time Data Fetching**: Continuously fetches weather data every 5 minutes.
- **Daily Weather Summaries**: Calculates daily average, maximum, minimum temperatures, and dominant weather conditions for each city.
- **Alert System**: User-defined thresholds trigger alerts, e.g., if the temperature exceeds 35°C.
- **Data Visualization**: Historical weather data is plotted for the last 7 days, showing average temperatures.

## Requirements

To run this project, you'll need the following Python packages:

bash
pip install requests schedule matplotlib
You also need to create a free account on OpenWeatherMap and obtain an API key.

## Setup and Usage
1. Clone the Repository

bash

git clone https://github.com/your-username/weather-monitoring-system.git
cd weather-monitoring-system

## 2. Add API Key

Replace 'your_openweathermap_api_key' in weather_app.py with your actual OpenWeatherMap API key.

## 3. Run the Application
python weather_app.py

## 4. Project Structure

weather_app/
│
├── weather_app.py            # Main script for running the weather monitoring system
├── weather.db                # SQLite database (created automatically after running)
├── README.md                 # Project documentation

## Functionality
Weather Data Fetching: The system fetches the current temperature, feels-like temperature, and weather condition (e.g., Clear, Rain) for each city every 5 minutes.
Daily Summaries: At the end of each day, the system calculates:
Average Temperature
Maximum and Minimum Temperatures
Dominant Weather Condition (based on frequency of weather conditions)
Alerting: The system checks every 5 minutes for any threshold violations, such as a temperature exceeding 35°C, and triggers an alert.
Data Visualization: The last 7 days' average temperature is plotted using Matplotlib.

