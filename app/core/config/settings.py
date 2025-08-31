from pydantic_settings import BaseSettings

class KakfaSettings(BaseSettings):
    KAFKA_BROKEN_URL: str
    KAFKA_TOPIC: str
    KAFKA_GROUP_ID: str
    
    class Config:
        case_sesitive=True
        env_file = '.env'
        extra = 'ignore'
        
        
kafka_setting = KakfaSettings()