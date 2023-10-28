from environs import Env

from pathlib import Path

ENV_FILE = ".env"
PATH_TO_ENV = Path().parent.joinpath(ENV_FILE)

class Config:

    env = Env()
    env.read_env(path=PATH_TO_ENV)

    BOT_TOKEN = env("BOT_TOKEN")




