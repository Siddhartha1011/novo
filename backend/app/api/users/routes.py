from fastapi import APIRouter, Depends

from app.api.auth.dependencies import get_current_user
from app.schemas.user import (
    ProfileResponse,
    ProfileUpdateRequest,
)
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=ProfileResponse,
)
def get_my_profile(
    current_user=Depends(get_current_user),
):

    return UserService.get_profile(
        current_user["id"]
    )


@router.patch(
    "/me",
    response_model=ProfileResponse,
)
def update_my_profile(
    data: ProfileUpdateRequest,
    current_user=Depends(get_current_user),
):

    return UserService.update_profile(
        user_id=current_user["id"],
        username=data.username,
        display_name=data.display_name,
        bio=data.bio,
        avatar_url=data.avatar_url,
    )