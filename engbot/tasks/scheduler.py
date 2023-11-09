from celery import Celery
from engbot.config import Config


scheduler = Celery(
    backend=f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/0",
    broker=f"amqp://{Config.RABBITMQ_USER}:{Config.RABBITMQ_PASSWORD}@{Config.RABBITMQ_HOST}:{Config.RABBITMQ_PORT}/",
)
