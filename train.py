from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score
import mlflow
import mlflow.sklearn

mlflow.set_experiment("iris-mlops")

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