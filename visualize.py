import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import pandas as pd


ALERT_TEMP_THRESHOLD = 35.0  # User-defined threshold for high temperature alerts
ALERT_CONSECUTIVE_THRESHOLD = 2  # Number of consecutive readings to trigger alert
def plot_daily_weather_summary():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()

    # Query daily weather summary data
    c.execute('''
        SELECT city, DATE(timestamp, 'unixepoch') as day, AVG(temperature), MAX(temperature), MIN(temperature)
        FROM weather
        GROUP BY city, day
    ''')

    results = c.fetchall()
    conn.close()

    # Organize the data for plotting
    days = []
    avg_temps = []
    max_temps = []
    min_temps = []
    cities = []

    for row in results:
        city, day, avg_temp, max_temp, min_temp = row
        days.append(day)
        avg_temps.append(avg_temp)
        max_temps.append(max_temp)
        min_temps.append(min_temp)
        cities.append(city)

    # Create a dataframe for easier plotting
    import pandas as pd
    df = pd.DataFrame({
        'Day': days,
        'Average Temp (°C)': avg_temps,
        'Max Temp (°C)': max_temps,
        'Min Temp (°C)': min_temps,
        'City': cities
    })

    # Plot the temperatures
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Day', y='Average Temp (°C)', hue='City', marker='o', label='Average Temperature')
    sns.lineplot(data=df, x='Day', y='Max Temp (°C)', hue='City', linestyle='--', label='Max Temperature')
    sns.lineplot(data=df, x='Day', y='Min Temp (°C)', hue='City', linestyle='--', label='Min Temperature')
    
    plt.title('Daily Weather Summary (Avg, Max, Min Temperatures)')
    plt.xticks(rotation=45)
    plt.xlabel('Day')
    plt.ylabel('Temperature (°C)')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()

# Call the function to generate the plot
plot_daily_weather_summary()


def plot_alerts():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()

    # Query daily weather summary and alert data
    c.execute('''
        SELECT city, DATE(timestamp, 'unixepoch') as day, AVG(temperature) as avg_temp
        FROM weather
        GROUP BY city, day
    ''')

    results = c.fetchall()
    conn.close()

    # Organize data
    days = []
    avg_temps = []
    cities = []
    alerts = []

    for row in results:
        city, day, avg_temp = row
        days.append(day)
        avg_temps.append(avg_temp)
        cities.append(city)
        # Check if the average temp exceeded the threshold
        if avg_temp > ALERT_TEMP_THRESHOLD:
            alerts.append(True)
        else:
            alerts.append(False)

    # Create dataframe
    df = pd.DataFrame({
        'Day': days,
        'Average Temp (°C)': avg_temps,
        'City': cities,
        'Alert': alerts
    })

    # Plot temperatures
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Day', y='Average Temp (°C)', hue='City', marker='o', label='Average Temperature')

    # Highlight days with alerts
    alert_days = df[df['Alert'] == True]
    plt.vlines(alert_days['Day'], ymin=df['Average Temp (°C)'].min(), ymax=df['Average Temp (°C)'].max(), colors='red', linestyles='dashed', label='Alert Threshold Breached')

    plt.title('Weather Summary with Alerts')
    plt.xticks(rotation=45)
    plt.xlabel('Day')
    plt.ylabel('Average Temperature (°C)')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()

# Call the function to plot alerts
plot_alerts()

# Function to visualize daily weather summary with alerts
def visualize_daily_weather_with_alerts():
    conn = sqlite3.connect('weather_data.db')
    cur = conn.cursor()

    # Query to get the daily summary (average, max, min temperatures) and alerts
    cur.execute('''
    SELECT city, AVG(temperature), MAX(temperature), MIN(temperature), timestamp
    FROM weather
    GROUP BY city, strftime('%Y-%m-%d', timestamp, 'unixepoch')
    ''')

    data = cur.fetchall()

    cities = {}
    for city, avg_temp, max_temp, min_temp, timestamp in data:
        if city not in cities:
            cities[city] = {"days": [], "avg": [], "max": [], "min": [], "alerts": []}

        cities[city]["days"].append(timestamp)
        cities[city]["avg"].append(avg_temp)
        cities[city]["max"].append(max_temp)
        cities[city]["min"].append(min_temp)

        # Check if an alert should be triggered (temp > threshold)
        if max_temp > 35:  # Replace with your alert threshold
            cities[city]["alerts"].append(True)
        else:
            cities[city]["alerts"].append(False)

    conn.close()

    # Plot the data for each city
    for city, data in cities.items():
        plt.figure(figsize=(10, 6))
        plt.plot(data["days"], data["avg"], label='Average Temp')
        plt.plot(data["days"], data["max"], label='Max Temp')
        plt.plot(data["days"], data["min"], label='Min Temp')

        # Highlight alert days with a red marker
        for i, alert in enumerate(data["alerts"]):
            if alert:
                plt.axvline(x=data["days"][i], color='red', linestyle='--', label='Alert')

        plt.title(f"Daily Weather Summary for {city}")
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.show()
visualize_daily_weather_with_alerts()
