import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

# Load dataset
df = pd.read_csv("../dataset/space_missions_dataset.csv")

# Remove missing values
df = df.dropna()

# Features
X = df[[
    "Payload Weight (tons)",
    "Fuel Consumption (tons)",
    "Mission Cost (billion USD)",
    "Mission Duration (years)",
    "Crew Size",
    "Scientific Yield (points)"
]]

# Target
y = df["Mission Success (%)"] > 85

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# Accuracy
pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, pred))

# Save model
pickle.dump(model, open("mission_model.pkl", "wb"))

print("Model trained and saved 🚀")