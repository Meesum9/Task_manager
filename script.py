import requests
import schedule
import time
import pywhatkit
from datetime import datetime

# Configuration
API_KEY = "4a1e50ce4a314a7993f150905250905"  # Your WeatherAPI.com API key
CITY = "Daejeon"  # Replace with your city
PHONE_NUMBER = "+821096161272"  # Replace with recipient's phone number (with country code, e.g., +1 for USA)
# Alternatively, use GROUP_NAME = "Your Group Name" for a WhatsApp group
SCHEDULE_TIME = "07:00"  # Time to send the message (24-hour format)

# Function to fetch weather data
def get_weather():
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=no"
        response = requests.get(url)
        data = response.json()

        if "error" not in data:
            weather = data["current"]["condition"]["text"]
            temp = data["current"]["temp_c"]
            feels_like = data["current"]["feelslike_c"]
            humidity = data["current"]["humidity"]
            wind_speed = data["current"]["wind_kph"]
            
            return f"Weather in {CITY} ({datetime.now().strftime('%Y-%m-%d')}):\n" \
                   f"Description: {weather}\n" \
                   f"Temperature: {temp}°C\n" \
                   f"Feels like: {feels_like}°C\n" \
                   f"Humidity: {humidity}%\n" \
                   f"Wind Speed: {wind_speed} km/h"
        else:
            return f"Error fetching weather data: {data['error']['message']}"
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"

# Function to send WhatsApp message
def send_whatsapp_message():
    weather_info = get_weather()
    try:
        # Get current hour and minute
        current_time = datetime.now()
        hour = current_time.hour
        minute = current_time.minute + 1  # Send message 1 minute from now
        
        # Send to a single contact
        pywhatkit.sendwhatmsg(
            phone_no=PHONE_NUMBER,
            message=weather_info,
            time_hour=hour,
            time_min=minute,
            wait_time=15,
            tab_close=True,
            close_time=5
        )
        print(f"Message scheduled for {PHONE_NUMBER}")
        # For a group, uncomment the line below and replace "Your Group Name"
        # pywhatkit.sendwhatmsg_to_group("Your Group Name", weather_info, int(SCHEDULE_TIME[:2]), int(SCHEDULE_TIME[3:]), 15, True, 5)
    except Exception as e:
        print(f"Error sending WhatsApp message: {str(e)}")

# Schedule the task to run daily
schedule.every().day.at(SCHEDULE_TIME).do(send_whatsapp_message)

# Keep the script running
while True:
    try:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\nScript stopped by user")
        break
    except Exception as e:
        print(f"Error in main loop: {str(e)}")
        time.sleep(60)  # Wait a minute before retrying