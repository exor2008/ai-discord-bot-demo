FROM python:3.11.3-slim-bullseye

WORKDIR /usr/src/app

COPY main.py .
COPY ai_discord_bot_demo ./ai_discord_bot_demo/
COPY pyproject.toml .
COPY README.md .

# For local runs
# COPY [".env", ".env"]

RUN pip install poetry
RUN poetry install --without dev

CMD ["poetry", "run", "python", "main.py"]