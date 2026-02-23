# app/api/v1/endpoints.py  (KEEP teammate file, but make it a proper router module)
from fastapi import APIRouter

from app.schemas.request import SensorInput
from app.services import xgb_service, ensemble_service, shap_service, rag_service

router = APIRouter()

@router.post("/ml/predict", tags=["ml"])
def predict(data: SensorInput):
    xgb_prob = xgb_service.predict_tabular([
        data.heart_rate,
        data.hrv,
        data.workload,
        data.gps_speed,
        data.acceleration,
        data.previous_injury,
    ])

    lstm_prob = 0.5
    final_risk = ensemble_service.fuse_predictions(xgb_prob, lstm_prob)

    explanation = shap_service.explain([
        data.heart_rate,
        data.hrv,
        data.workload,
        data.gps_speed,
        data.acceleration,
        data.previous_injury,
    ])

    advice = rag_service.get_recovery_advice(f"Player risk score {final_risk}")

    return {
        "injury_risk": final_risk,
        "shap_values": explanation,
        "recovery_advice": advice,
    }