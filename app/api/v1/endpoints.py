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

router = APIRouter()


# ----------------------------
# Risk Classification Function
# ----------------------------
def classify_risk(score: float) -> str:
    if score < 0.35:
        return "Low"
    elif score < 0.65:
        return "Moderate"
    return "High"


@router.post("/predict")
def predict(data: SensorInput, db: Session = Depends(get_db)):

    # ----------------------------
    # 1. Save current session
    # ----------------------------
    session = PlayerSession(
        athlete_id=data.athlete_id,
        heart_rate=data.heart_rate,
        body_temperature=data.body_temperature,
        hydration_level=data.hydration_level,
        sleep_quality=data.sleep_quality,
        recovery_score=data.recovery_score,
        stress_level=data.stress_level,
        muscle_activity=data.muscle_activity,
        joint_angles=data.joint_angles,
        gait_speed=data.gait_speed,
        cadence=data.cadence,
        step_count=data.step_count,
        jump_height=data.jump_height,
        ground_reaction_force=data.ground_reaction_force,
        range_of_motion=data.range_of_motion,
        ambient_temperature=data.ambient_temperature,
        humidity=data.humidity,
        altitude=data.altitude,
        training_intensity=data.training_intensity,
        training_duration=data.training_duration,
        training_load=data.training_load,
        fatigue_index=data.fatigue_index,
        injury_occurred=data.injury_occurred
    )

    db.add(session)
    db.commit()

    # ----------------------------
    # 2. Fetch athlete history
    # ----------------------------
    history = (
        db.query(PlayerSession)
        .filter(PlayerSession.athlete_id == data.athlete_id)
        .order_by(PlayerSession.id)
        .all()
    )

    if len(history) < 3:
        return {
            "message": "Not enough historical data for prediction",
            "sessions_recorded": len(history)
        }

    # ----------------------------
    # 3. Convert to DataFrame
    # ----------------------------
    df = pd.DataFrame([h.__dict__ for h in history])
    df = df.drop(columns=["_sa_instance_state"])

    # ----------------------------
    # 4. Feature Engineering
    # ----------------------------
    engineered = build_features(df)

    latest_row = engineered.iloc[-1].to_dict()
    latest_row.pop("injury_occurred", None)

    # ----------------------------
    # 5–8. Safe Prediction Block
    # ----------------------------
    try:
        xgb_prob = predict_tabular(latest_row)
        lstm_prob = predict_sequence(data.sequence)
        final_risk = fuse_predictions(xgb_prob, lstm_prob)
        risk_level = classify_risk(final_risk)

    except Exception as e:
        return {
            "error": "Prediction failed",
            "details": str(e)
        }

    return {
        "injury_risk": final_risk,
        "risk_level": risk_level,
        "xgb_risk": xgb_prob,
        "lstm_risk": lstm_prob
    }