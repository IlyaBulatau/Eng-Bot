from environs import Env

from pathlib import Path
import sys
import os
from enum import Enum


DEBUG = "DEBUG"

class EnvFile(Enum):
    """
    Set of env files
    """
    DEV = ".env"
    TEST = ".env.test"
    PROD = ".env.prod"


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
        if DEBUG == False - .env.prod
        Return path to env file
        """
        debug = os.getenv(DEBUG, 0)
        
        if int(debug) == 0:    
            self.env_file = EnvFile.PROD.value
        else:
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
    manager = RunManager()
    env.read_env(path=manager.get_env())

    BOT_TOKEN = env("BOT_TOKEN")
    DATABASE_URL = env("DATABASE_URL")
    MONGO_DB_NAME = env("MONGO_DB_NAME")
    MONGO_COLLECTION_NAME = env("MONGO_COLLECTION_NAME")

    REDIS_HOST = env("REDIS_HOST")
    REDIS_PORT = env("REDIS_PORT")
