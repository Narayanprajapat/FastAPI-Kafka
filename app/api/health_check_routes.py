from fastapi import APIRouter, status
from app.schemas.health_check import Response

health_check_router = APIRouter()

@health_check_router.get("/health_check", response_model=Response)
def health():
    return Response(message='Server is Running', status_code=status.HTTP_200_OK)
    