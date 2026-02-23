import shap
import joblib

model = joblib.load("app/models/xgb_model.pkl")
explainer = shap.TreeExplainer(model)

def explain(features):
    shap_values = explainer.shap_values([features])
    return shap_values[0].tolist()