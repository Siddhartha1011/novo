from fastapi import HTTPException

from app.services.supabase import supabase


class UserService:

    @staticmethod
    def get_profile(user_id: str):

        response = (
            supabase
            .table("profiles")
            .select(
                "id, username, display_name, avatar_url, bio"
            )
            .eq("id", user_id)
            .single()
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Profile not found.",
            )

        return response.data


    @staticmethod
    def update_profile(
        user_id: str,
        username: str | None = None,
        display_name: str | None = None,
        bio: str | None = None,
        avatar_url: str | None = None,
    ):

        updates = {}

        if username is not None:
            updates["username"] = username.strip().lower()

        if display_name is not None:
            updates["display_name"] = display_name

        if bio is not None:
            updates["bio"] = bio

        if avatar_url is not None:
            updates["avatar_url"] = avatar_url

        if not updates:
            raise HTTPException(
                status_code=400,
                detail="No profile changes provided.",
            )

        response = (
            supabase
            .table("profiles")
            .update(updates)
            .eq("id", user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Profile not found.",
            )

        return response.data[0]