from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse, UserPublic
from app.core.security import hash_password, verify_password, create_access_token
from app.services.store import store
from fastapi import Depends
from app.core.deps import get_current_user

router = APIRouter()


@router.post("/signup", response_model=UserPublic)
def signup(req: SignupRequest) -> UserPublic:
    existing = store.get_user_by_email(req.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = store.create_user(req.name, req.email, hash_password(req.password), req.role)
    return UserPublic(id=user["id"], name=user["name"], email=user["email"], role=user["role"])


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest) -> TokenResponse:
    user = store.get_user_by_email(req.email)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user["id"], role=user["role"])
    return TokenResponse(access_token=token, role=user["role"])

@router.get("/me", response_model=UserPublic)
def me(user: UserPublic = Depends(get_current_user)) -> UserPublic:
    return user