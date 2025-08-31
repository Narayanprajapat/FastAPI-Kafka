from app.models.users import User
from sqlalchemy.future import select
from typing import Iterable, Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import UserCreate, UserOut


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: UserCreate) -> UserOut:
        user = User(name=data.name, email=data.email)
        self.db.add(user)
        try:
            await self.db.commit()
            await self.db.refresh(user)
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("User with this email already exists")
        return UserOut.model_validate(user)

    async def get(self, user_id: int) -> Optional[UserOut]:
        res = await self.db.execute(select(User).where(User.id == user_id))
        user = res.scalar_one_or_none()
        return UserOut.model_validate(user) if user else None

    async def list(self) -> Iterable[UserOut]:
        res = await self.db.execute(select(User))
        users = res.scalars().all()
        return [UserOut.model_validate(u) for u in users]
