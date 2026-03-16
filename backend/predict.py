import pickle

# =========================
# Load trained ML model
# =========================
model = pickle.load(open("mission_model.pkl", "rb"))


# =========================
# Prediction Function
# =========================
def predict_mission(payload):

    try:

        payload = float(payload)

        # Limit payload to realistic range
        if payload < 1:
            payload = 1
        if payload > 1000:
            payload = 1000

        # Model expects 6 features
        data = [[
            payload,   # Payload Weight (tons)
            200,       # Fuel Consumption (tons)
            10,        # Mission Cost (billion USD)
            5,         # Mission Duration (years)
            4,         # Crew Size
            70         # Scientific Yield
        ]]

        prob = model.predict_proba(data)[0][1]

        success_percent = round(prob * 100, 2)
        failure_percent = round((1 - prob) * 100, 2)

        if prob > 0.6:
            status = "Mission Success 🚀"
        else:
            status = "Risky Mission ⚠️"

        return {
            "status": status,
            "success": success_percent,
            "failure": failure_percent
        }

    except Exception as e:
        return {
            "error": str(e)
        }