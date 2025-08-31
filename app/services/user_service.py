from app.schemas.users import UserCreate, UserOut
from app.repository.user_repository import UserRepository
from app.core.messaging.kafka.producer import KafkaProducer
from app.core.config.settings import kafka_producer_setting


class UserService:
    def __init__(self, repo: UserRepository, producer: KafkaProducer):
        self.repo = repo
        self.producer = producer

    async def create_user(self, data: UserCreate) -> UserOut:
        user = await self.repo.create(data)
        # Send Kafka event
        self.producer.send_json(
            topic=kafka_producer_setting.KAFKA_TOPIC,
            payload={"event": "user_created", "user": user.model_dump()},
            key=f"user-{user.id}",
        )
        return user

    async def get_user(self, user_id: int) -> UserOut | None:
        return await self.repo.get(user_id)

    async def list_users(self) -> list[UserOut]:
        return await self.repo.list()
