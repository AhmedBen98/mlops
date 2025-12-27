from sklearn.datasets import load_iris
import pandas as pd
import os

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Load iris dataset
iris = load_iris(as_frame=True)
# Create DataFrame
df = iris.frame
# Rename 'target' column to 'species'
df = df.rename(columns={'target': 'species'})
# Save to CSV
df.to_csv("data/iris.csv", index=False)
print("iris.csv generated successfully")
