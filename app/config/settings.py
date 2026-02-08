from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    
    ELEVENLABS_API_KEY: str
    REDIS_URL: str
    TEMP_MEDIA_DIR: str
    OUTPUTS_DIR: str
