FROM python:3.11.3-slim-bullseye

RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user
ENV PATH="$PATH:/home/user/.local/bin"

COPY main.py .
COPY ai_discord_bot_demo ./ai_discord_bot_demo/
COPY pyproject.toml .
COPY README.md .

# For local runs
# COPY [".env", ".env"]

RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry install
RUN poetry show

CMD ["poetry", "run", "python", "main.py"]