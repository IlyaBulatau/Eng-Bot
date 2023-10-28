from environs import Env

from pathlib import Path
import sys
from enum import Enum


class RunManager:
    """
    Set up before run
    """

    def __init__(self):
        self.env_file = EnvFile.DEV.value

    def get_env(self) -> Path:
        """
        get env file
        if pytest is runner - env file will = ".evn.test"
        Return path to env file
        """

        runner = sys.argv[0].split("/")[-1].strip()
        if runner == "pytest":
            # if run pytest .
            self.env_file = EnvFile.TEST.value

        path_to_env = Path().parent.joinpath(self.env_file)
        return path_to_env


class Config:
    """
    Basically class for keep environments veriables
    """

    env = Env()
    path_to_env = RunManager().get_env()
    env.read_env(path=path_to_env)

    BOT_TOKEN = env("BOT_TOKEN")
    DATABASE_URL = env("DATABASE_URL")
    MONGO_DB_NAME = env("MONGO_DB_NAME")
    MONGO_COLLECTION_NAME = env("MONGO_COLLECTION_NAME")


class EnvFile(Enum):
    """
    Set of env files
    """

    DEV = ".env"
    TEST = ".env.test"
