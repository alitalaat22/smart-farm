import os
import time
import random
import datetime
import requests
import logging
from flask import Flask, render_template
from dotenv import load_dotenv

# تحميل الإعدادات من ملف .env
load_dotenv()

# إعدادات النظام
MOISTURE_THRESHOLD = int(os.getenv("MOISTURE_THRESHOLD", 35))
TEMP_WARNING = 38
USE_SOLAR = os.getenv("USE_SOLAR", "True") == "True"
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_LOCATION = "Cairo,EG"

app = Flask(__name__)

# إعداد نظام التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("farm.log"),
        logging.StreamHandler()
    ],
    datefmt='%Y-%m-%d %H:%M:%S'  # أضف هذا السطر
)

class SmartIrrigation:
    def __init__(self):
        self.is_on = False
    
    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            logging.info("✅ تشغيل نظام الري")
    
    def turn_off(self):
        if self.is_on:
            self.is_on = False
            logging.info("🛑 إيقاف نظام الري")

def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={WEATHER_LOCATION}&appid={WEATHER_API_KEY}&units=metric&lang=ar"
        response = requests.get(url, timeout=10)
        data = response.json()
        return {
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description']
        }
    except Exception as e:
        logging.error(f"خطأ في الطقس: {str(e)}")
        return None

@app.route('/')
def dashboard():
    weather = get_weather()
    return render_template('dashboard.html', 
    weather=weather,
    now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)

if __name__ == "__main__":
    irrigation = SmartIrrigation()
    try:
        while True:
            moisture = random.randint(20, 80)
            temp = random.uniform(25, 42)
            
            if moisture < MOISTURE_THRESHOLD:
                irrigation.turn_on()
            else:
                irrigation.turn_off()
            
            logging.info(f"الرطوبة: {moisture}% - الحرارة: {temp:.1f}°C")
            time.sleep(5)
            
    except KeyboardInterrupt:
        logging.info("إيقاف النظام")
