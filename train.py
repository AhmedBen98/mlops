from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score
import pandas as pd
import pickle
import os

# Load the dataset
data = pd.read_csv("data/iris.csv")
X = data.drop("species", axis=1)
y = data["species"]

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save the model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved as model.pkl")

# Ensure the output directory exists
os.makedirs("data/processed", exist_ok=True)

# Generate the preprocessed file
data.to_csv("data/processed/preprocessed.csv", index=False)
print("Preprocessed data saved to data/processed/preprocessed.csv")