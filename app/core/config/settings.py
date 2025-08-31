from pydantic_settings import BaseSettings


class KakfaConsumerSettings(BaseSettings):
    KAFKA_BROKEN_URL: str
    KAFKA_TOPIC: str
    KAFKA_GROUP_ID: str

    class Config:
        case_sesitive = True
        env_file = ".env"
        extra = "ignore"


class KakfaProducerSettings(BaseSettings):
    KAFKA_BROKEN_URL: str
    CLIENT_ID: str = "python-producer"
    KAFKA_TOPIC: str

    class Config:
        case_sesitive = True
        env_file = ".env"
        extra = "ignore"


class PostgresqlSettings(BaseSettings):
    HOST: str
    USERNAME: str
    PASSWORD: str
    PORT: str


postgresql_settings = PostgresqlSettings()
kafka_consumer_setting = KakfaConsumerSettings()
kafka_producer_setting = KakfaProducerSettings()
