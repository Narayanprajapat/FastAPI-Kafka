from fastapi import APIRouter
from app.api.health_check_routes import health_check_router

routers = APIRouter()

routers.include_router(router=health_check_router, tags=['Health Check'])
