from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.assistant import router as assistant_router
from app.api.v1.athletes import router as athletes_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.players import router as players_router
from app.api.v1.predictions import router as predictions_router
from app.api.v1.wearables import router as wearables_router
from app.api.v1.endpoints import router as ml_router  # teammate file

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(assistant_router, prefix="/assistant", tags=["assistant"])
api_router.include_router(athletes_router, prefix="/athletes", tags=["athletes"])
api_router.include_router(players_router, prefix="/players", tags=["players"])
api_router.include_router(predictions_router, prefix="/predictions", tags=["predictions"])
api_router.include_router(wearables_router, prefix="/wearables", tags=["wearables"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(ml_router, tags=["ml"])