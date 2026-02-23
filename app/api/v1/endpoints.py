from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd

from app.schemas.request import SensorInput
from app.db.database import get_db
from app.db.models import PlayerSession
from app.services.feature_pipeline import build_features
from app.services.xgb_service import predict_tabular
from app.services.lstm_service import predict_sequence
from app.services.ensemble_service import fuse_predictions

# Optional services (don’t fail if teammate didn’t implement them)
try:
    from app.services import shap_service, rag_service
except Exception:
    shap_service = None
    rag_service = None

router = APIRouter()

def classify_risk(score: float) -> str:
    if score < 0.35:
        return "Low"
    elif score < 0.65:
        return "Moderate"
    return "High"


@router.post("/ml/predict", tags=["ml"])
def predict(data: SensorInput, db: Session = Depends(get_db)):
    payload = data.model_dump()

    # ----------------------------
    # 1. Save current session
    # ----------------------------
    session = PlayerSession(
        athlete_id=payload.get("athlete_id"),
        heart_rate=payload.get("heart_rate"),
        body_temperature=payload.get("body_temperature"),
        hydration_level=payload.get("hydration_level"),
        sleep_quality=payload.get("sleep_quality"),
        recovery_score=payload.get("recovery_score"),
        stress_level=payload.get("stress_level"),
        muscle_activity=payload.get("muscle_activity"),
        joint_angles=payload.get("joint_angles"),
        gait_speed=payload.get("gait_speed"),
        cadence=payload.get("cadence"),
        step_count=payload.get("step_count"),
        jump_height=payload.get("jump_height"),
        ground_reaction_force=payload.get("ground_reaction_force"),
        range_of_motion=payload.get("range_of_motion"),
        ambient_temperature=payload.get("ambient_temperature"),
        humidity=payload.get("humidity"),
        altitude=payload.get("altitude"),
        training_intensity=payload.get("training_intensity"),
        training_duration=payload.get("training_duration"),
        training_load=payload.get("training_load"),
        fatigue_index=payload.get("fatigue_index"),
        injury_occurred=payload.get("injury_occurred"),
    )

    db.add(session)
    db.commit()

    # ----------------------------
    # 2. Fetch athlete history
    # ----------------------------
    history = (
        db.query(PlayerSession)
        .filter(PlayerSession.athlete_id == payload.get("athlete_id"))
        .order_by(PlayerSession.id)
        .all()
    )

    if len(history) < 3:
        return {
            "message": "Not enough historical data for prediction",
            "sessions_recorded": len(history),
        }

    # ----------------------------
    # 3. Convert to DataFrame
    # ----------------------------
    df = pd.DataFrame([h.__dict__ for h in history]).drop(columns=["_sa_instance_state"])

    # ----------------------------
    # 4. Feature Engineering
    # ----------------------------
    engineered = build_features(df)

    latest_row = engineered.iloc[-1].to_dict()
    latest_row.pop("injury_occurred", None)

    # ----------------------------
    # 5–8. Prediction
    # ----------------------------
    try:
        xgb_prob = predict_tabular(latest_row)
        seq = payload.get("sequence")
        lstm_prob = predict_sequence(seq) if seq is not None else 0.5
        final_risk = fuse_predictions(xgb_prob, lstm_prob)
        risk_level = classify_risk(final_risk)
    except Exception as e:
        return {"error": "Prediction failed", "details": str(e)}

    # ----------------------------
    # 9. Optional explainability + advice
    # ----------------------------
    explanation = None
    advice = None

    if shap_service is not None:
        try:
            explanation = shap_service.explain(latest_row)
        except Exception:
            explanation = None

    if rag_service is not None:
        try:
            advice = rag_service.get_recovery_advice(
                f"Athlete risk score {final_risk} ({risk_level}). Key features: {list(latest_row.keys())[:10]}"
            )
        except Exception:
            advice = None

    return {
        "injury_risk": final_risk,
        "risk_level": risk_level,
        "xgb_risk": xgb_prob,
        "lstm_risk": lstm_prob,
        "shap_values": explanation,
        "recovery_advice": advice,
    }