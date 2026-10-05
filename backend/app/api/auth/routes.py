from fastapi import APIRouter

from app.schemas.auth import (
    LoginRequest,
    SignupRequest,
    TokenResponse,
)
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/signup")
def signup(data: SignupRequest):

    user = AuthService.signup(
        email=str(data.email),
        password=data.password,
        username=data.username,
        display_name=data.display_name,
    )

    return {
        "message": (
            "Account created. "
            "Please verify your email before logging in."
        ),
        "user_id": user.id,
        "email": user.email,
    }


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(data: LoginRequest):

    response = AuthService.login(
        email=str(data.email),
        password=data.password,
    )

    return TokenResponse(
        access_token=response.session.access_token,
        refresh_token=response.session.refresh_token,
        token_type="bearer",
        user_id=response.user.id,
        email=response.user.email,
    )