from pydantic import BaseModel
from typing import List

class SensorInput(BaseModel):
    heart_rate : float
    hrv: float
    workload: float
    gps_speed: float
    acceleration: float
    previous_injury: int