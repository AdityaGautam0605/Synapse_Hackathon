from typing import Optional
from pydantic import BaseModel


class WearableConnectRequest(BaseModel):
    provider: str


class WearableStatusResponse(BaseModel):
    connected: bool
    provider: Optional[str] = None
    last_sync: Optional[str] = None