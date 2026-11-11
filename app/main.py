
from fastapi import FastAPI

from app.core.config import settings
from app.routers import user_routes
from app.routers import address_routes

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="ShopEase User Management Microservice"
)


@app.get("/")
def root():
    return {
        "message": "ShopEase User Management Service is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "user-management-service"
    }


app.include_router(user_routes.router)

app.include_router(address_routes.router)