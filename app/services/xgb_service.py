import joblib
import numpy as np
import pandas as pd

model = joblib.load("app/models/xgb_model.pkl")
scaler = joblib.load("app/models/xgb_scaler.pkl")
feature_names = joblib.load("app/models/xgb_features.pkl")


def predict_tabular(features_dict):

   
    row = []

    for col in feature_names:
        value = features_dict.get(col, 0.0)
        row.append(value)

    
    df = pd.DataFrame([row], columns=feature_names)

    df = df.fillna(0.0)
    df = df.replace([np.inf, -np.inf], 0.0)

   
    df = df.clip(-1e6, 1e6)

    
    arr_scaled = scaler.transform(df)

   
    prob = model.predict_proba(arr_scaled)[0][1]

    return float(prob)