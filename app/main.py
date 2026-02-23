from fastapi import FastAPI
from app.api.v1.endpoints import router
from app.ml.model_registry import registry
from app.db.database import engine
from app.db import models

app = FastAPI(title="KinetIQ Backend")


@app.on_event("startup")
def startup_event():
    registry.load_models()
    models.Base.metadata.create_all(bind=engine)


app.include_router(router, prefix="/api/v1")