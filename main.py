import asyncio
import os

from dotenv import load_dotenv

from bot import client

if __name__ == "__main__":
    load_dotenv()

    client.run(os.environ["DISCORD_TOKEN"])
