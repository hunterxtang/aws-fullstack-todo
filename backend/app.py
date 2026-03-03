import os
import requests
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

todos = {}
next_id = 1

@app.get("/")
def home():
    return "todo backend running"

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/api/info")
def info():
    return jsonify({
        "service": "todo-api",
        "time": int(time.time()),
        "count": len(todos)
    })

@app.get("/api/todos")
def list_todos():
    items = list(todos.values())
    items.sort(key=lambda x: x["id"])
    return jsonify({"items": items})

@app.get("/api/weather")
def weather():
    lat = float(request.args.get("lat", os.environ.get("DEFAULT_LAT", "34.0224")))
    lon = float(request.args.get("lon", os.environ.get("DEFAULT_LON", "-118.2851")))

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph"
    }

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    current = data.get("current", {})
    return jsonify({
        "latitude": lat,
        "longitude": lon,
        "temperature_f": current.get("temperature_2m"),
        "humidity_percent": current.get("relative_humidity_2m"),
        "wind_mph": current.get("wind_speed_10m"),
        "time": current.get("time")
    })

@app.post("/api/todos")
def create_todo():
    global next_id
    body = request.get_json(silent=True) or {}
    text = (body.get("text") or "").strip()
    if len(text) == 0:
        return jsonify({"error": "text is required"}), 400

    item = {"id": next_id, "text": text, "done": False}
    todos[next_id] = item
    next_id = next_id + 1
    return jsonify(item), 201

@app.patch("/api/todos/<int:todo_id>")
def toggle_todo(todo_id):
    if todo_id not in todos:
        return jsonify({"error": "not found"}), 404
    body = request.get_json(silent=True) or {}
    if "done" in body:
        todos[todo_id]["done"] = bool(body["done"])
    if "text" in body:
        text = (body["text"] or "").strip()
        if len(text) == 0:
            return jsonify({"error": "text cannot be empty"}), 400
        todos[todo_id]["text"] = text
    return jsonify(todos[todo_id])

@app.delete("/api/todos/<int:todo_id>")
def delete_todo(todo_id):
    if todo_id not in todos:
        return jsonify({"error": "not found"}), 404
    deleted = todos.pop(todo_id)
    return jsonify(deleted)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
