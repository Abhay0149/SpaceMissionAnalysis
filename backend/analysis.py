import pandas as pd
import matplotlib.pyplot as plt
import pickle

from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# ===============================
# Load Dataset
# ===============================

file_path = "../dataset/space_missions_dataset.csv"
df = pd.read_csv(file_path)

print("\n===== Dataset Preview =====\n")
print(df.head())

print("\nTotal Missions:", len(df))


# ===============================
# Data Cleaning
# ===============================

df = df.dropna()

df["Payload Weight (tons)"] = df["Payload Weight (tons)"].astype(float)
df["Mission Success (%)"] = df["Mission Success (%)"].astype(float)


# ===============================
# Mission Type Analysis
# ===============================

mission_types = df["Mission Type"].value_counts()

plt.figure(figsize=(8,5))
plt.bar(mission_types.index, mission_types.values)

plt.title("Mission Type Distribution")
plt.xlabel("Mission Type")
plt.ylabel("Number of Missions")

plt.tight_layout()
plt.show()


# ===============================
# Launch Vehicle Analysis
# ===============================

launch_vehicle = df["Launch Vehicle"].value_counts()

plt.figure(figsize=(8,5))
plt.bar(launch_vehicle.index, launch_vehicle.values)

plt.title("Launch Vehicle Usage")
plt.xlabel("Launch Vehicle")
plt.ylabel("Number of Missions")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


# ===============================
# Target Type Analysis
# ===============================

target_planet = df["Target Type"].value_counts()

plt.figure(figsize=(8,5))
plt.bar(target_planet.index, target_planet.values)

plt.title("Target Type Distribution")
plt.xlabel("Target Type")
plt.ylabel("Number of Missions")

plt.tight_layout()
plt.show()


# ===============================
# Space Mission Summary
# ===============================

total_missions = len(df)
avg_payload = df["Payload Weight (tons)"].mean()
avg_success = df["Mission Success (%)"].mean()

print("\n===== Space Mission Summary =====")

print("Total Missions:", total_missions)
print("Average Payload Weight:", round(avg_payload,2))
print("Average Mission Success Rate:", round(avg_success,2))


# ===============================
# Feature Engineering
# ===============================

df["Mission Type"] = df["Mission Type"].astype("category").cat.codes
df["Launch Vehicle"] = df["Launch Vehicle"].astype("category").cat.codes
df["Target Type"] = df["Target Type"].astype("category").cat.codes


# ===============================
# Machine Learning Prediction
# ===============================

X = df[[
"Payload Weight (tons)",
"Mission Type",
"Launch Vehicle",
"Target Type"
]]

y = df["Mission Success (%)"] > 80


X_train, X_test, y_train, y_test = train_test_split(
X,
y,
test_size=0.2,
random_state=42
)

model = RandomForestClassifier(
n_estimators=100,
random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

print("\nModel Accuracy:", round(accuracy,3))


# ===============================
# Save Model (IMPORTANT)
# ===============================

pickle.dump(model, open("mission_model.pkl","wb"))

print("\nModel saved successfully as mission_model.pkl")


# ===============================
# Anomaly Detection
# ===============================

iso = IsolationForest(
contamination=0.1,
random_state=42
)

df["anomaly"] = iso.fit_predict(
df[["Payload Weight (tons)", "Mission Success (%)"]]
)

risky = df[df["anomaly"] == -1]

print("\nRisky Missions Detected:", len(risky))


# ===============================
# Payload Distribution
# ===============================

plt.figure(figsize=(8,5))

plt.hist(df["Payload Weight (tons)"], bins=10)

plt.title("Payload Weight Distribution")
plt.xlabel("Payload Weight (tons)")
plt.ylabel("Frequency")

plt.tight_layout()
plt.show()