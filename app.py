from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY", "affd554b8138bf4fef309c984651cbbf")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/image/<filename>")
def serve_image(filename):
    return send_from_directory("image", filename)

@app.route("/api/weather")
def api_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "위도/경도가 필요합니다"}), 400

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=kr"
    )
    r = requests.get(url, timeout=5)
    data = r.json()

    return jsonify({
        "temp": round(data["main"]["temp"]),
        "desc": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"]
    })

if __name__ == "__main__":
    app.run(debug=True)
