# Example: https://lynn-kwong.medium.com/how-to-use-pydantic-to-read-environment-variables-and-secret-files-in-python-8a6b8c56381c

from typing import List

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    admins: List[str] = ["353057906"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
