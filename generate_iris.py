from sklearn.datasets import load_iris
import pandas as pd

# Load iris dataset
iris = load_iris(as_frame=True)
# Create DataFrame
df = iris.frame
# Save to CSV
df.to_csv("data/iris.csv", index=False)
print("iris.csv generated successfully")
