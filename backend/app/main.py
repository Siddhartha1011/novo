from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.users import router as users_router


app = FastAPI(
    title="Novo API",
    description="Backend API for the Novo social media application",
    version="0.1.0",
)


app.include_router(auth_router)
app.include_router(users_router)


@app.get("/")
def root():
    return {
        "message": "Novo API is running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }