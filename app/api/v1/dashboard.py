from fastapi import APIRouter, Depends
from app.core.deps import get_current_user, require_role
from app.schemas.auth import UserPublic
from app.services.store import store

router = APIRouter()


@router.get("/coach")
def coach_dashboard(user: UserPublic = Depends(require_role("coach"))):
    athletes = store.list_athletes_for_coach(user.id)
    latest = []
    for a in athletes:
        p = store.get_latest_prediction(a["id"])
        if p:
            latest.append({"athlete_id": a["id"], "name": a["name"], "risk_score": p["risk_score"], "band": p["band"]})
    latest_sorted = sorted(latest, key=lambda x: x["risk_score"], reverse=True)[:10]
    return {"coach_id": user.id, "athletes_count": len(athletes), "top_risk": latest_sorted}


@router.get("/player")
def player_dashboard(user: UserPublic = Depends(require_role("player"))):
    athlete = None
    for a in store.athletes.values():
        if a.get("player_user_id") == user.id:
            athlete = a
            break
    if not athlete:
        return {"player_id": user.id, "linked_athlete": None}

    pred = store.get_latest_prediction(athlete["id"])
    return {"player_id": user.id, "linked_athlete": athlete["id"], "latest_prediction": pred}