from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title = "Injury & Fatigue Prediction API")

app.include_router(router)