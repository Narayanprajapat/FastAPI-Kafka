from app.core.config.settings import postgresql_settings
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

database_url = f"postgresql+asyncpg://{postgresql_settings.USERNAME}:{postgresql_settings.PASSWORD}@{postgresql_settings.HOST}:{postgresql_settings.PORT}/appdb"


engine = create_async_engine(database_url, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
