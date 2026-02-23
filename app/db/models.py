from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from app.db.database import Base


class PlayerSession(Base):
    __tablename__ = "player_sessions"

    id = Column(Integer, primary_key=True, index=True)
    athlete_id = Column(Integer, index=True)

    # Biometric
    heart_rate = Column(Float)
    body_temperature = Column(Float)
    hydration_level = Column(Float)
    sleep_quality = Column(Float)
    recovery_score = Column(Float)
    stress_level = Column(Float)
    muscle_activity = Column(Float)
    joint_angles = Column(Float)
    gait_speed = Column(Float)
    cadence = Column(Float)
    step_count = Column(Float)
    jump_height = Column(Float)
    ground_reaction_force = Column(Float)
    range_of_motion = Column(Float)

    # Environment
    ambient_temperature = Column(Float)
    humidity = Column(Float)
    altitude = Column(Float)
    playing_surface = Column(String)

    # Training load
    training_intensity = Column(Float)
    training_duration = Column(Float)
    training_load = Column(Float)
    fatigue_index = Column(Float)

    # Demographics
    sport_type = Column(String)
    gender = Column(String)
    age = Column(Float)
    bmi = Column(Float)

    # Injury label (optional for logging)
    injury_occurred = Column(Integer, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)