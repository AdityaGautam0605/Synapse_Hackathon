from fastapi import APIRouter, Depends, HTTPException, status
from app.core.deps import require_role
from app.schemas.auth import UserPublic
from app.schemas.biometrics import BiometricsIngestRequest, BiometricsResponse
from app.services.store import store

router = APIRouter()


def _get_linked_athlete_id(user_id: str) -> str:
    for a in store.athletes.values():
        if a.get("player_user_id") == user_id:
            return a["id"]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No athlete profile linked to this player")


@router.post("/me/biometrics", response_model=BiometricsResponse)
def ingest_biometrics(req: BiometricsIngestRequest, user: UserPublic = Depends(require_role("player"))):
    athlete_id = _get_linked_athlete_id(user.id)
    item = {"athlete_id": athlete_id, **req.model_dump()}
    store.add_biometrics(athlete_id, item)
    return BiometricsResponse(**item)


@router.get("/me/biometrics", response_model=list[BiometricsResponse])
def list_biometrics(limit: int = 100, user: UserPublic = Depends(require_role("player"))):
    athlete_id = _get_linked_athlete_id(user.id)
    items = store.get_biometrics(athlete_id, limit=limit)
    return [BiometricsResponse(**x) for x in items]