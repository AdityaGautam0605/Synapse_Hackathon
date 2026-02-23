from fastapi import APIRouter, Depends
from app.core.deps import require_role
from app.schemas.auth import UserPublic
from app.schemas.wearables import WearableConnectRequest, WearableStatusResponse
from app.services.store import store

router = APIRouter()


@router.post("/connect", response_model=WearableStatusResponse)
def connect(req: WearableConnectRequest, user: UserPublic = Depends(require_role("player"))):
    s = store.wearable_connect(user.id, req.provider)
    return WearableStatusResponse(**s)


@router.post("/sync", response_model=WearableStatusResponse)
def sync(user: UserPublic = Depends(require_role("player"))):
    s = store.wearable_sync(user.id)
    return WearableStatusResponse(**s)


@router.get("/status", response_model=WearableStatusResponse)
def status(user: UserPublic = Depends(require_role("player"))):
    s = store.wearable_status(user.id)
    return WearableStatusResponse(**s)