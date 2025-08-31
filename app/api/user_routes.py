from fastapi import APIRouter, Depends
from app.core.db.postgresql import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import UserCreate, UserOut
from app.services.user_service import UserService
from app.repository.user_repository import UserRepository
from app.core.messaging.kafka.producer import KafkaProducer

user_router = APIRouter(prefix="/users")

producer = KafkaProducer()


def get_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo=repo, producer=producer)


@user_router.post("", response_model=UserOut, status_code=201)
async def create_user(payload: UserCreate, service: UserService = Depends(get_service)):
    return await service.create_user(payload)


@user_router.get("/{user_id}", response_model=UserOut | None)
async def get_user(user_id: int, service: UserService = Depends(get_service)):
    return await service.get_user(user_id)


@user_router.get("", response_model=list[UserOut])
async def list_users(service: UserService = Depends(get_service)):
    return await service.list_users()
