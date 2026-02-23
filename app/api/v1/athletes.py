from fastapi import APIRouter, Depends, HTTPException, status
from app.core.deps import require_role
from app.schemas.auth import UserPublic
from app.schemas.athletes import AthleteCreateRequest, AthletePatchRequest, AthleteResponse
from app.services.store import store

router = APIRouter()


@router.post("", response_model=AthleteResponse)
def create_athlete(req: AthleteCreateRequest, user: UserPublic = Depends(require_role("coach"))):
    athlete = store.create_athlete(user.id, req.model_dump())
    return AthleteResponse(**athlete)


@router.get("", response_model=list[AthleteResponse])
def list_athletes(user: UserPublic = Depends(require_role("coach"))):
    athletes = store.list_athletes_for_coach(user.id)
    return [AthleteResponse(**a) for a in athletes]


@router.get("/{athlete_id}", response_model=AthleteResponse)
def get_athlete(athlete_id: str, user: UserPublic = Depends(require_role("coach"))):
    athlete = store.get_athlete(athlete_id)
    if not athlete or athlete["coach_id"] != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Athlete not found")
    return AthleteResponse(**athlete)


@router.patch("/{athlete_id}", response_model=AthleteResponse)
def patch_athlete(athlete_id: str, req: AthletePatchRequest, user: UserPublic = Depends(require_role("coach"))):
    athlete = store.get_athlete(athlete_id)
    if not athlete or athlete["coach_id"] != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Athlete not found")
    updated = store.update_athlete(athlete_id, req.model_dump())
    return AthleteResponse(**updated)