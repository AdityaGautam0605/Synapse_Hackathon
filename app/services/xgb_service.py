import numpy as np
from app.ml.model_registry import registry


def predict_tabular(feature_dict: dict) -> float:
    """
    feature_dict: dictionary of engineered feature_name -> value
    Must match training feature names.
    """

    model = registry.xgb_model
    scaler = registry.scaler
    feature_names = registry.feature_names

    # Ensure correct feature order
    ordered = [feature_dict.get(f, 0) for f in feature_names]

    arr = np.array(ordered).reshape(1, -1)

    # Apply same scaling used during training
    arr_scaled = scaler.transform(arr)

    prob = model.predict_proba(arr_scaled)[0][1]

    return float(prob)