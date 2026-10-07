from pydantic import BaseModel, Field


class ProfileResponse(BaseModel):
    id: str
    username: str
    display_name: str | None
    avatar_url: str | None
    bio: str | None


class ProfileUpdateRequest(BaseModel):
    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=30,
    )
    display_name: str | None = Field(
        default=None,
        max_length=100,
    )
    bio: str | None = Field(
        default=None,
        max_length=500,
    )
    avatar_url: str | None = None