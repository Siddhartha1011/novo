from fastapi import HTTPException

from app.services.supabase import supabase


class AuthService:

    @staticmethod
    def signup(
        email: str,
        password: str,
        username: str,
        display_name: str | None = None,
    ):

        email = email.strip().lower()
        username = username.strip().lower()

        existing_username = (
            supabase
            .table("profiles")
            .select("id")
            .eq("username", username)
            .limit(1)
            .execute()
        )

        if existing_username.data:
            raise HTTPException(
                status_code=409,
                detail="Username is already taken.",
            )

        try:
            response = supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                    "options": {
                        "data": {
                            "username": username,
                            "display_name": display_name,
                        }
                    },
                }
            )

        except Exception as exc:

            message = str(exc).lower()

            if (
                "already registered" in message
                or "already exists" in message
            ):
                raise HTTPException(
                    status_code=409,
                    detail="An account already exists for this email.",
                )

            raise HTTPException(
                status_code=400,
                detail="Unable to create account.",
            )

        if not response.user:
            raise HTTPException(
                status_code=400,
                detail="Unable to create account.",
            )

        return response.user

    @staticmethod
    def login(
        email: str,
        password: str,
    ):

        email = email.strip().lower()

        try:
            response = supabase.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password,
                }
            )

        except Exception:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password.",
            )

        if not response.user or not response.session:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password.",
            )

        if not response.user.email_confirmed_at:
            raise HTTPException(
                status_code=403,
                detail="Please verify your email before logging in.",
            )

        return response
    
    @staticmethod
    def forgot_password(email: str):

        email = email.strip().lower()

        try:
            supabase.auth.reset_password_for_email(
                email,
                {
                    "redirect_to": "http://localhost:3000/reset-password"
                },
            )

        except Exception:
            pass

        return {
            "message": (
                "If an account exists for this email, "
                "a password reset link has been sent."
            )
        }


    @staticmethod
    def resend_verification(email: str):

        email = email.strip().lower()

        try:
            supabase.auth.resend(
                {
                    "type": "signup",
                    "email": email,
                    "options": {
                        "email_redirect_to": "http://localhost:3000/verify-email"
                    },
                }
            )

        except Exception:
            # Don't reveal whether an account exists.
            pass

        return {
            "message": (
                "If the account requires verification, "
                "a verification email has been sent."
            )
        }
        