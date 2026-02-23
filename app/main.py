from fastapi import FastAPI
from app.api.v1.main import router as v1_router
from app.core.config import settings

app = FastAPI(title="Kinetiq API", version=settings.VERSION)
app.include_router(v1_router, prefix=settings.API_V1_PREFIX)