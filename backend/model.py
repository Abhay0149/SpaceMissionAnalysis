import pandas as pd
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# ======================
# Load dataset
# ======================
df = pd.read_csv("../dataset/space_missions_dataset.csv")

# remove missing values
df = df.dropna()


# ======================
# Convert categorical columns
# ======================
df["Mission Type"] = df["Mission Type"].astype("category").cat.codes
df["Launch Vehicle"] = df["Launch Vehicle"].astype("category").cat.codes
df["Target Type"] = df["Target Type"].astype("category").cat.codes


# ======================
# Features
# ======================
X = df[[
    "Payload Weight (tons)",
    "Mission Type",
    "Launch Vehicle",
    "Target Type"
]]

# success if mission success > 80%
y = df["Mission Success (%)"] > 80


# ======================
# Train model
# ======================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)


# ======================
# Model accuracy
# ======================
pred = model.predict(X_test)
accuracy = accuracy_score(y_test, pred)

print("\nModel Accuracy:", round(accuracy, 3))


# ======================
# Save model
# ======================
with open("mission_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nModel trained and saved successfully as mission_model.pkl")