from pydantic import BaseModel
from typing import List, Optional


class SensorInput(BaseModel):
    athlete_id: int

    # 30 x 99 pose sequence
    sequence: List[List[float]]

    # Current tabular row
    heart_rate: float
    body_temperature: float
    hydration_level: float
    sleep_quality: float
    recovery_score: float
    stress_level: float
    muscle_activity: float
    joint_angles: float
    gait_speed: float
    cadence: float
    step_count: float
    jump_height: float
    ground_reaction_force: float
    range_of_motion: float
    ambient_temperature: float
    humidity: float
    altitude: float
    training_intensity: float
    training_duration: float
    training_load: float
    fatigue_index: float

    injury_occurred: Optional[int] = None