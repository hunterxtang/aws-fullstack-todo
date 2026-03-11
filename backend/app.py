import os
import requests
import time
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

app = Flask(__name__)
CORS(app)

# --- Astra DB setup ---
cloud_config = {'secure_connect_bundle': '/app/secure-connect-bundle.zip'}
auth_provider = PlainTextAuthProvider(
    os.environ['ASTRA_CLIENT_ID'],
    os.environ['ASTRA_CLIENT_SECRET']
)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('todo')

# Create table if it doesn't exist
session.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id uuid PRIMARY KEY,
        text text,
        done boolean,
        created_at timestamp
    )
""")

# --- Routes ---

@app.get("/")
def home():
    return "todo backend running"

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/api/info")
def info():
    count = session.execute("SELECT COUNT(*) FROM todos").one()[0]
    return jsonify({
        "service": "todo-api",
        "time": int(time.time()),
        "count": count
    })

@app.get("/api/todos")
def list_todos():
    rows = session.execute("SELECT id, text, done FROM todos")
    items = [{"id": str(r.id), "text": r.text, "done": r.done} for r in rows]
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
    body = request.get_json(silent=True) or {}
    text = (body.get("text") or "").strip()
    if len(text) == 0:
        return jsonify({"error": "text is required"}), 400
    new_id = uuid.uuid4()
    session.execute(
        "INSERT INTO todos (id, text, done, created_at) VALUES (%s, %s, %s, toTimestamp(now()))",
        (new_id, text, False)
    )
    return jsonify({"id": str(new_id), "text": text, "done": False}), 201

@app.patch("/api/todos/<todo_id>")
def toggle_todo(todo_id):
    uid = uuid.UUID(todo_id)
    row = session.execute("SELECT * FROM todos WHERE id=%s", (uid,)).one()
    if not row:
        return jsonify({"error": "not found"}), 404
    body = request.get_json(silent=True) or {}
    done = bool(body["done"]) if "done" in body else row.done
    text = row.text
    if "text" in body:
        text = (body["text"] or "").strip()
        if len(text) == 0:
            return jsonify({"error": "text cannot be empty"}), 400
    session.execute(
        "UPDATE todos SET done=%s, text=%s WHERE id=%s",
        (done, text, uid)
    )
    return jsonify({"id": todo_id, "text": text, "done": done})

@app.delete("/api/todos/<todo_id>")
def delete_todo(todo_id):
    uid = uuid.UUID(todo_id)
    row = session.execute("SELECT * FROM todos WHERE id=%s", (uid,)).one()
    if not row:
        return jsonify({"error": "not found"}), 404
    session.execute("DELETE FROM todos WHERE id=%s", (uid,))
    return jsonify({"id": todo_id, "text": row.text, "done": row.done})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
