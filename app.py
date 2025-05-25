from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def dashboard():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {
            "temp": "غير متوفر",
            "humidity": "غير متوفر",
            "moisture": "غير متوفر",
            "weather_temp": "غير متوفر",
            "weather_humidity": "غير متوفر",
            "weather_desc": "غير متوفر",
            "power_source": "غير متوفر"
        }
    return render_template("dashboard.html", **data)

if __name__ == '__main__':
    app.run(debug=True)
