from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    LOG_LEVEL: str
    DB_TYPE: str

    REMOTE_DB_USER: str
    REMOTE_DB_PASS: str

    LOCAL_DB_HOST: str
    LOCAL_DB_PORT: int

    DB_BOX: str
    DB_COLLECTION: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def REMOTE_DATABASE_URL(self):
        return f"mongodb+srv://{self.REMOTE_DB_USER}:{self.REMOTE_DB_PASS}@cluster0.xe1smep.mongodb.net/"

    @property
    def LOCAL_DATABASE_URL(self):
        return f"mongodb://{self.LOCAL_DB_HOST}:{self.LOCAL_DB_PORT}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
