from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    config = load_config()
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = {}
    data["power_source"] = "طاقة شمسية" if config["use_solar"] else "كهرباء"
    data["irrigation_on"] = config["irrigation_on"]
    data["sensors"] = config["sensors"]
    return render_template("dashboard.html", data=data)

@app.route("/toggle_power", methods=["POST"])
def toggle_power():
    config = load_config()
    source = request.json.get("source")
    config["use_solar"] = (source == "solar")
    save_config(config)
    return jsonify({"status": "ok"})

@app.route("/toggle_irrigation", methods=["POST"])
def toggle_irrigation():
    config = load_config()
    config["irrigation_on"] = not config["irrigation_on"]
    save_config(config)
    return jsonify({"status": "ok", "irrigation_on": config["irrigation_on"]})

@app.route("/toggle_sensor", methods=["POST"])
def toggle_sensor():
    sensor_name = request.json.get("sensor")
    config = load_config()
    current = config["sensors"].get(sensor_name, True)
    config["sensors"][sensor_name] = not current
    save_config(config)
    return jsonify({"status": "ok", "sensor": sensor_name, "enabled": not current})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
