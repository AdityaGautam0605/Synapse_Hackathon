from typing import Optional
from pydantic import BaseModel


class BiometricsIngestRequest(BaseModel):
    timestamp: str
    hr: Optional[float] = None
    hrv: Optional[float] = None
    sleep_hours: Optional[float] = None
    rpe: Optional[float] = None
    soreness: Optional[float] = None
    stress: Optional[float] = None
    accel_load: Optional[float] = None
    distance_km: Optional[float] = None
    steps: Optional[float] = None


class BiometricsResponse(BiometricsIngestRequest):
    athlete_id: str