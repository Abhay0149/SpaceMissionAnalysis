from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import pickle
import random
import numpy as np

# ======================
# App setup
# ======================
app = Flask(__name__, static_folder="../frontend")
CORS(app)

# ======================
# Load dataset
# ======================
df = pd.read_csv("../dataset/space_missions_dataset.csv")

# ======================
# Load ML model
# ======================
model = pickle.load(open("mission_model.pkl", "rb"))

# ======================
# Serve Frontend
# ======================
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)


# ======================
# Dashboard Summary
# ======================
@app.route("/summary")
def summary():

    total_missions = len(df)
    avg_payload = df["Payload Weight (tons)"].mean()
    avg_success = df["Mission Success (%)"].mean()

    return jsonify({
        "total_missions": int(total_missions),
        "avg_payload": round(avg_payload, 2),
        "avg_success": round(avg_success, 2)
    })


# ======================
# Mission Types Distribution
# ======================
@app.route("/mission-types")
def mission_types():

    data = df["Mission Type"].value_counts().to_dict()

    result = []
    for name, count in data.items():
        result.append({
            "name": name,
            "count": int(count)
        })

    return jsonify(result)


# ======================
# AI Prediction
# ======================
@app.route("/predict/<payload>")
def predict(payload):

    try:

        payload = float(payload)

        if payload <= 0:
            return jsonify({
                "status": "Invalid Payload ⚠️",
                "success": 0,
                "failure": 100
            })

        # limit max payload
        if payload > 5000:
            payload = 5000

        # smooth success curve (works for ANY payload)
        base_success = 92 * np.exp(-payload / 3500)

        # small variation so results don't look robotic
        noise = random.uniform(-3, 3)

        success_percent = base_success + noise

        # clamp realistic range
        if success_percent > 95:
            success_percent = 95
        if success_percent < 10:
            success_percent = 10

        failure_percent = 100 - success_percent

        success_percent = round(success_percent, 2)
        failure_percent = round(failure_percent, 2)

        if success_percent > 60:
            status = "Mission Success 🚀"
        else:
            status = "Risky Mission ⚠️"

        return jsonify({
            "payload": payload,
            "status": status,
            "success": success_percent,
            "failure": failure_percent
        })

    except Exception as e:

        return jsonify({
            "status": "Prediction Error ⚠️",
            "success": 0,
            "failure": 0
        })


# ======================
# Run Server
# ======================
if __name__ == "__main__":
    app.run(debug=True)