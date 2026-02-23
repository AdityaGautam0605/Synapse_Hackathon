from typing import Literal
from pydantic import BaseModel, EmailStr, Field


Role = Literal["coach", "player"]


class SignupRequest(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=6)
    role: Role


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: Role


class UserPublic(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: Role