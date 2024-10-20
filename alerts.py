import smtplib
from email.mime.text import MIMEText
import sqlite3

# Function to send an email
def send_email_alert(city, temperature, timestamp):
    sender = 'your_email@example.com'
    recipient = 'recipient_email@example.com'
    subject = f"Weather Alert: High Temperature in {city}"
    body = f"ALERT: The temperature in {city} exceeded the threshold at {temperature}°C. Time: {timestamp}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        # Setup the server connection
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, 'your_email_password')  # Use App Password if needed
            server.sendmail(sender, recipient, msg.as_string())
            print(f"Email sent to {recipient} regarding {city}'s high temperature!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Modify the check_for_alerts function to include email alert
def check_for_alerts():
    conn = sqlite3.connect('weather_data.db')
    cur = conn.cursor()

    # Query to get the last two temperature updates for each city
    cur.execute('''
    SELECT city, temperature, timestamp 
    FROM weather 
    ORDER BY timestamp DESC 
    LIMIT 2
    ''')

    recent_data = cur.fetchall()

    # Define the alert threshold (e.g., temperature exceeds 35°C)
    alert_threshold = 35

    for city, temperature, timestamp in recent_data:
        if temperature > alert_threshold:
            print(f"ALERT: {city} temperature exceeded {alert_threshold}°C at {timestamp}")
            send_email_alert(city, temperature, timestamp)  # Send email alert
    
    conn.close()

check_for_alerts()    
