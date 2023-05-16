FROM python:3.11.3-slim-bullseye

WORKDIR usr/src/app

RUN apt update && apt install -y git
RUN git clone https://github.com/exor2008/ai-discord-bot-demo.git .

COPY [".env", ".env"]

RUN pip install poetry
RUN poetry install --no-root --without dev

CMD ["poetry", "run", "python", "main.py"]