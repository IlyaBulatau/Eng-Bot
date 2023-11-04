FROM python:3.10.6-buster

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /code/bot

RUN pip install poetry --no-cache-dir && \
    poetry config virtualenvs.create false

COPY . .

RUN poetry install --no-interaction --no-ansi

COPY bot-entrypoint.sh .

RUN chmod 777 bot-entrypoint.sh

ENTRYPOINT [ "./bot-entrypoint.sh" ]