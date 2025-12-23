from sklearn.datasets import load_iris
import pandas as pd

# Load iris dataset
iris = load_iris(as_frame=True)
# Create DataFrame
df = iris.frame
# Rename 'target' column to 'species'
df = df.rename(columns={'target': 'species'})
# Save to CSV
df.to_csv("data/iris.csv", index=False)
print("iris.csv generated successfully")
