from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field


RiskBand = Literal["low", "medium", "high"]


class PredictionRunRequest(BaseModel):
    athlete_id: Optional[str] = None


class PredictionResponse(BaseModel):
    prediction_id: str
    athlete_id: str
    timestamp: str
    risk_score: float
    band: RiskBand
    zones: Dict[str, float] = Field(default_factory=dict)


class PredictionHistoryResponse(BaseModel):
    items: List[PredictionResponse] = Field(default_factory=list)