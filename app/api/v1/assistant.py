from fastapi import APIRouter, Depends, HTTPException, status
from app.core.deps import get_current_user, require_owner_or_self
from app.schemas.auth import UserPublic
from app.schemas.assistant import AssistantPromptRequest, AssistantPromptResponse
from app.services.store import store

router = APIRouter()

@router.post("/prompt", response_model=AssistantPromptResponse)
def prompt(req: AssistantPromptRequest, user: UserPublic = Depends(get_current_user)):
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

    pred = store.get_latest_prediction(athlete_id)
    if not pred:
        return AssistantPromptResponse(reply="No prediction found yet. Run a prediction first.")

    score = pred["risk_score"]
    band = pred["band"]
    zones = pred.get("zones", {})
    top_zone = None
    if zones:
        top_zone = sorted(zones.items(), key=lambda x: x[1], reverse=True)[0][0]

    reply = f"Your current risk is {band} (score={round(score, 2)})."
    if top_zone:
        reply += f" The most stressed area appears to be {top_zone.replace('_', ' ')}."
    reply += " Consider reducing intensity, prioritizing sleep, and monitoring soreness over the next 24–48 hours."

    return AssistantPromptResponse(reply=reply)