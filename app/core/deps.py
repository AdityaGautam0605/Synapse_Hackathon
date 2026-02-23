from typing import Literal, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_token
from app.services.store import store
from app.schemas.auth import UserPublic

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserPublic:
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        role = payload.get("role")
        if not user_id or role not in ("coach", "player"):
            raise ValueError("bad token")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = store.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return UserPublic(id=user["id"], name=user["name"], email=user["email"], role=user["role"])


def require_role(required: Literal["coach", "player"]):
    def _inner(user: UserPublic = Depends(get_current_user)) -> UserPublic:
        if user.role != required:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return user

    return _inner


def require_owner_or_self(athlete_id: str, user: UserPublic) -> None:
    athlete = store.get_athlete(athlete_id)
    if not athlete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Athlete not found")

    if user.role == "coach":
        if athlete["coach_id"] != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return

    if user.role == "player":
        if athlete.get("player_user_id") != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")