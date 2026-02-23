from typing import List, Optional
from pydantic import BaseModel, Field


class AthleteCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    age: Optional[int] = None
    sex: Optional[str] = None
    position: Optional[str] = None
    injury_history: List[str] = Field(default_factory=list)
    player_user_id: Optional[str] = None
    recent_performance: Optional[str] = None


class AthletePatchRequest(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    position: Optional[str] = None
    injury_history: Optional[List[str]] = None
    player_user_id: Optional[str] = None
    recent_performance: Optional[str] = None


class AthleteResponse(BaseModel):
    id: str
    coach_id: str
    name: str
    age: Optional[int] = None
    sex: Optional[str] = None
    position: Optional[str] = None
    injury_history: List[str] = Field(default_factory=list)
    player_user_id: Optional[str] = None
    recent_performance: Optional[str] = None