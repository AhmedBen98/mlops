from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# Test multiple values for n_estimators
for n_estimators in [10, 20, 30, 40, 50, 100, 150, 200, 250]:
    model = RandomForestClassifier(n_estimators=n_estimators)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    print(f"n_estimators: {n_estimators}, Accuracy: {accuracy_score(y_test, preds)}")