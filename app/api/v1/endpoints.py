from fastapi import APIRouter
from app.schemas import SensorInput
from app.services import (
    feature_service,
    xgb_service,
    lstm_service,
    ensemble_service,
    shap_service,
    rag_service
)

router = APIRouter()

@router.post("/predict")
def predict(data: SensorInput):

    # Tabular prediction
    xgb_prob = xgb_service.predict_tabular([
        data.heart_rate,
        data.hrv,
        data.workload,
        data.gps_speed,
        data.acceleration,
        data.previous_injury
    ])

    # Dummy LSTM for now
    lstm_prob = 0.5

    # Ensemble
    final_risk = ensemble_service.fuse_predictions(xgb_prob, lstm_prob)

    # SHAP
    explanation = shap_service.explain([
        data.heart_rate,
        data.hrv,
        data.workload,
        data.gps_speed,
        data.acceleration,
        data.previous_injury
    ])

    # RAG advice
    advice = rag_service.get_recovery_advice(
        f"Player risk score {final_risk}"
    )

    return {
        "injury_risk": final_risk,
        "shap_values": explanation,
        "recovery_advice": advice
    }