import schedule
import time
from weather import get_weather  # Assuming fetch_weather_data is in weather.py
from alerts import check_for_alerts
from visualize import visualize_daily_weather_with_alerts

# Schedule to fetch weather data every 5 minutes
schedule.every(5).minutes.do(get_weather)

# Schedule to check alerts every 5 minutes
schedule.every(5).minutes.do(check_for_alerts)

# Schedule to visualize the daily summary once per day (e.g., at 6 PM)
schedule.every().day.at("18:00").do(visualize_daily_weather_with_alerts)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
