# نظام ذكي متكامل لإدارة أرض زراعية بمساحة 6 قيراط
# يدعم: حساسات بيئية + تحكم في الري + إنذارات + لوحة تحكم + طاقة شمسية/كهرباء + تحليل AI + ربط بحالة الطقس

import time
import random  # تُستبدل لاحقًا بالحساسات الفعلية
import datetime
import requests
import logging
import json

# --- إعدادات النظام من ملف خارجي ---
with open("config.json", "r", encoding="utf-8") as config_file:
    CONFIG = json.load(config_file)

MOISTURE_THRESHOLD = CONFIG["moisture_threshold"]
TEMP_WARNING = CONFIG["temp_warning"]
USE_SOLAR = CONFIG["use_solar"]
ENABLE_ALERTS = CONFIG["enable_alerts"]
WEATHER_API_KEY = CONFIG["weather_api_key"]
WEATHER_LOCATION = CONFIG["weather_location"]

# --- إعدادات تسجيل الأحداث ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# --- محاكاة الحساسات ---
def read_soil_moisture():
    value = random.randint(20, 80)
    if 0 <= value <= 100:
        return value
    logger.warning("قيمة رطوبة التربة غير منطقية: %s", value)
    return 50

def read_temperature():
    value = round(random.uniform(25, 42), 1)
    if 10 <= value <= 60:
        return value
    logger.warning("درجة حرارة غير منطقية: %s", value)
    return 30.0

def read_humidity():
    value = random.randint(30, 90)
    if 0 <= value <= 100:
        return value
    logger.warning("رطوبة جو غير منطقية: %s", value)
    return 60

# --- تحليل AI بسيط للتنبؤ باحتياج الري ---
def predict_irrigation_need(moisture, temp, humidity):
    score = (100 - moisture) + (temp - 25) * 1.5 - (humidity - 50) * 0.5
    return score > 30

# --- نظام إنذار ---
def send_alert(message):
    if ENABLE_ALERTS:
        logger.warning(f"🔔 إشعار: {message}")

# --- نظام الطاقة ---
def check_power_source():
    return "☀️ طاقة شمسية" if USE_SOLAR else "⚡ كهرباء عادية"

# --- نظام الري ---
class SmartIrrigation:
    def __init__(self):
        self.is_on = False

    def turn_on(self):
        if not self.is_on:
            self.is_on = True
            logger.info("✅ تشغيل نظام الري")

    def turn_off(self):
        if self.is_on:
            self.is_on = False
            logger.info("🛑 إيقاف نظام الري")

# --- جلب حالة الطقس من API خارجي ---
def get_weather_forecast():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={WEATHER_LOCATION}&appid={WEATHER_API_KEY}&units=metric&lang=ar"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        return temp, humidity, description
    except Exception as e:
        logger.error(f"خطأ في جلب بيانات الطقس: {e}")
        return None, None, "فشل في جلب بيانات الطقس"

# --- لوحة التحكم عبر واجهة مبسطة (تمثل موبايل أو لابتوب) ---
def dashboard_loop():
    irrigation = SmartIrrigation()
    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temp = read_temperature()
        humidity = read_humidity()
        moisture = read_soil_moisture()
        weather_temp, weather_humidity, weather_desc = get_weather_forecast()

        logger.info(f"🧠 [{now}] تحديث البيانات:")
        logger.info(f"🔌 مصدر الطاقة: {check_power_source()}")
        logger.info(f"🌡 درجة الحرارة (من الحساس): {temp}°C")
        logger.info(f"💧 رطوبة الجو (من الحساس): {humidity}%")
        logger.info(f"🌱 رطوبة التربة: {moisture}%")
        logger.info(f"🌥 حالة الطقس من الإنترنت: {weather_desc} | حرارة: {weather_temp}°C | رطوبة: {weather_humidity}%")

        if weather_temp and abs(temp - weather_temp) > 5:
            send_alert("فرق كبير بين حرارة الحساس وتوقع الطقس")

        if moisture < MOISTURE_THRESHOLD or predict_irrigation_need(moisture, temp, humidity):
            irrigation.turn_on()
        else:
            irrigation.turn_off()

        if temp > TEMP_WARNING:
            send_alert("درجة حرارة مرتفعة! راقب المحصول")

        time.sleep(5)

# --- بدء التشغيل ---
if __name__ == "__main__":
    logger.info("🚀 بدء تشغيل النظام الذكي المتكامل لإدارة الأرض الزراعية...")
    try:
        dashboard_loop()
    except KeyboardInterrupt:
        logger.info("🛑 تم إيقاف النظام يدويًا")
