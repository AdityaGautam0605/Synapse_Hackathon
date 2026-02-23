import joblib 
import numpy as np

model = joblib.load("app/models/xgb_model.pkl")

def predict_tabular(features):
    arr = np.array(features).reshape(1,-1)
    prob = model.predict_proba(arr)[0][1]
    return prob
