from redis import Redis

from engbot.config import Config


redis_cli = Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
