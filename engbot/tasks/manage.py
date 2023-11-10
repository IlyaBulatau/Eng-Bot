from datetime import datetime, timedelta
from random import choice

from engbot.tasks import constants as con
from engbot.tasks import tasks
from engbot.services.cache.states import CacheTaskId

from celery.result import AsyncResult


class TaskManager:
    """
    Manager of tasks
    Run, delete and traces for tasks
    """

    TASK_PREFIX = "task_notice_about_learn"
    TASK_SEP = ":"

    def __init__(self, user_telegram_id: int | str):
        self.user_telegram_id = str(user_telegram_id)
        self.task_name = self.TASK_PREFIX + self.TASK_SEP + self.user_telegram_id

        self.datetime_now = datetime.now()
        self.morning_notice_time = timedelta(hours=con.MORNING_TIME[1])
        self.evening_notice_time = timedelta(hours=con.EVENING_TIME[0])

    def notice_about_learn(self):
        cache = CacheTaskId(self.task_name)
        old_task_id = cache.get_task()

        if old_task_id:
            AsyncResult(id=old_task_id).revoke()

        result: AsyncResult = tasks.notice_user_about_learn.apply_async(
            (self.user_telegram_id,), eta=self._eta_calculate(), shadow=self.task_name
        )

        cache.set_task(result.id)

    def _eta_calculate(self) -> datetime:
        """
        Calculates time for send notice.

        In case if time now + 12 hour is between 11 - 18 hour,
        notice will send at 18 or 19 o'clock.
        Otherwise message send at 10 or 11 o'clock
        """
        notice_time: datetime = self.datetime_now + timedelta(
            hours=con.NOTICE_INTERVAL_HOUR
        )
        time_to_notice: datetime = (
            datetime(
                year=notice_time.year,
                month=notice_time.month,
                day=notice_time.day,
                hour=choice(con.EVENING_TIME),
            )
            if self.morning_notice_time
            < timedelta(hours=notice_time.hour)
            < self.evening_notice_time
            else datetime(
                year=notice_time.year,
                month=notice_time.month,
                day=notice_time.day,
                hour=choice(con.MORNING_TIME),
            )
            if timedelta(hours=notice_time.hour) < self.morning_notice_time
            else datetime(
                year=notice_time.year,
                month=notice_time.month,
                day=notice_time.day + 1,
                hour=choice(con.MORNING_TIME),
            )
        )

        return time_to_notice
