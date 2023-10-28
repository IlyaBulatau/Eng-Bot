from environs import Env

from pathlib import Path

ENV_FILE = ".env"
PATH_TO_ENV = Path().parent.joinpath(ENV_FILE)

class Config:

    env = Env()
    env.read_env(path=PATH_TO_ENV)

    BOT_TOKEN = env("BOT_TOKEN")
    DATABASE_URL = env("DATABASE_URL")
    MONGO_DB_NAME = env("MONGO_DB_NAME")
    MONGO_COLLECTION_NAME = env("MONGO_COLLECTION_NAME")


