import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

data = pd.DataFrame({
    "hours": [1,2,3,4,5],
    "attendance": [60,70,80,90,95],
    "sleep": [5,6,7,8,9],
    "prev_marks": [40,50,60,70,80],
    "marks": [45,55,65,75,85]
})

X = data[["hours","attendance","sleep","prev_marks"]]
y = data["marks"]

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "model.pkl")

print("Model trained successfully!")
