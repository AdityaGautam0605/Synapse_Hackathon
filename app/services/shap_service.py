import shap
import joblib
import pandas as pd
import numpy as np

model = joblib.load("app/models/xgb_model.pkl")
feature_names = joblib.load("app/models/xgb_features.pkl")

explainer = shap.TreeExplainer(model)


def explain(features_dict, top_k: int = 5):
    # Build ordered dataframe
    row = []
    for col in feature_names:
        row.append(features_dict.get(col, 0.0))

    df = pd.DataFrame([row], columns=feature_names)
    df = df.replace([np.inf, -np.inf], 0)
    df = df.fillna(0)

    shap_values = explainer.shap_values(df)

    # For binary classification
    if isinstance(shap_values, list):
        shap_values = shap_values[1]

    shap_values = shap_values[0]

    results = []

    for feature, value in zip(feature_names, shap_values):
        results.append({
            "feature": feature,
            "impact": float(value),
            "abs_impact": abs(float(value))
        })

    # Sort by absolute impact
    results.sort(key=lambda x: x["abs_impact"], reverse=True)

    # Keep top_k
    top_features = results[:top_k]

    # Add direction field
    formatted = []
    for item in top_features:
        formatted.append({
            "feature": item["feature"],
            "impact": item["impact"],
            "direction": "increases_risk" if item["impact"] > 0 else "decreases_risk"
        })

    return formatted