from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score
import mlflow
import mlflow.sklearn
import pandas as pd
import pickle
import os

mlflow.set_experiment("iris-mlops")

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

# Loop through different values of n_estimators
for n_estimators in [10, 20, 30, 40]:
    with mlflow.start_run():
        X, y = load_iris(return_X_y=True)
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=123)
        model = RandomForestClassifier(n_estimators=n_estimators, random_state=123)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        precision = precision_score(y_test, preds, average='weighted')

        # Log parameters, metrics, and model to MLFlow
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", precision)
        mlflow.sklearn.log_model(model, "model")

        print(f"n_estimators: {n_estimators}, Accuracy: {acc}, Precision: {precision}")