from typing import Optional
from pydantic import BaseModel


class AssistantPromptRequest(BaseModel):
    prompt: str
    athlete_id: Optional[str] = None


class AssistantPromptResponse(BaseModel):
    reply: str