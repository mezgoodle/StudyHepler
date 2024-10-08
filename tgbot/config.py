from typing import List

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr
    access_id: SecretStr
    access_key: SecretStr
    bucket_name: str = "studyhelper"
    region_name: str = "eu-central-1"
    admins: List[int] = [353057906]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


config = Settings()
