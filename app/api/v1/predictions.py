from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.deps import get_current_user, require_owner_or_self
from app.schemas.auth import UserPublic
from app.schemas.predictions import PredictionRunRequest, PredictionResponse, PredictionHistoryResponse
from app.services.store import store

router = APIRouter()


def _band(score: float) -> str:
    if score < 0.33:
        return "low"
    if score < 0.66:
        return "medium"
    return "high"


def _fake_predict(athlete_id: str) -> PredictionResponse:
    bio = store.get_biometrics(athlete_id, limit=20)
    base = 0.2
    for x in bio[-5:]:
        base += 0.02 * (x.get("rpe") or 0)
        base += 0.02 * (x.get("soreness") or 0)
        base -= 0.01 * (x.get("sleep_hours") or 0)
        base -= 0.005 * (x.get("hrv") or 0)
    score = max(0.0, min(1.0, base))
    zones = {
        "left_knee": min(1.0, score + 0.10),
        "right_knee": max(0.0, score - 0.05),
        "left_hamstring": min(1.0, score + 0.05),
        "right_hamstring": max(0.0, score - 0.10),
        "lower_back": min(1.0, score + 0.02),
        "shoulder": max(0.0, score - 0.12),
    }
    pred = PredictionResponse(
        prediction_id=str(uuid4()),
        athlete_id=athlete_id,
        timestamp=store.now(),
        risk_score=score,
        band=_band(score),
        zones=zones,
    )
    return pred


@router.post("/run", response_model=PredictionResponse)
def run(req: PredictionRunRequest, user: UserPublic = Depends(get_current_user)):
    athlete_id = req.athlete_id
    if user.role == "player":
        athlete_id = None
        for a in store.athletes.values():
            if a.get("player_user_id") == user.id:
                athlete_id = a["id"]
                break
        if not athlete_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No athlete profile linked")

    if user.role == "coach":
        if not athlete_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="athlete_id required for coach")

    require_owner_or_self(athlete_id, user)

    pred = _fake_predict(athlete_id)
    store.add_prediction(athlete_id, pred.model_dump())
    return pred


@router.get("/latest", response_model=PredictionResponse)
def latest(athlete_id: str, user: UserPublic = Depends(get_current_user)):
    require_owner_or_self(athlete_id, user)
    pred = store.get_latest_prediction(athlete_id)
    if not pred:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No prediction yet")
    return PredictionResponse(**pred)


@router.get("/history", response_model=PredictionHistoryResponse)
def history(athlete_id: str, limit: int = 30, user: UserPublic = Depends(get_current_user)):
    require_owner_or_self(athlete_id, user)
    items = store.get_prediction_history(athlete_id, limit=limit)
    return PredictionHistoryResponse(items=[PredictionResponse(**x) for x in items])


@router.get("/{prediction_id}/heatmap")
def heatmap(athlete_id: str, prediction_id: str, user: UserPublic = Depends(get_current_user)):
    require_owner_or_self(athlete_id, user)
    items = store.get_prediction_history(athlete_id, limit=200)
    for x in items[::-1]:
        if x.get("prediction_id") == prediction_id:
            return {"athlete_id": athlete_id, "prediction_id": prediction_id, "zones": x.get("zones", {})}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prediction not found")