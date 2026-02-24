
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api_router import api_router

from app.ml.model_registry import registry
from app.db.database import engine
from app.db import models

app = FastAPI(title="Kinetiq API", version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.on_event("startup")
def startup_event():
    registry.load_models()
    models.Base.metadata.create_all(bind=engine)