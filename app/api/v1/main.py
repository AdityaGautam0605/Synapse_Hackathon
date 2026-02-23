from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.athletes import router as athletes_router
from app.api.v1.players import router as players_router
from app.api.v1.wearables import router as wearables_router
from app.api.v1.predictions import router as predictions_router
from app.api.v1.assistant import router as assistant_router

from app.api.v1.endpoints import router as core_router  # your /predict

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
router.include_router(athletes_router, prefix="/athletes", tags=["athletes"])
router.include_router(players_router, prefix="/players", tags=["players"])
router.include_router(wearables_router, prefix="/wearables", tags=["wearables"])
router.include_router(predictions_router, prefix="/predictions", tags=["predictions"])
router.include_router(assistant_router, prefix="/assistant", tags=["assistant"])

# keep your teammate's predict endpoint
router.include_router(core_router, tags=["predict"])