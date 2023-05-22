import os

from dotenv import load_dotenv

from ai_discord_bot_demo.bot import bot
from ai_discord_bot_demo.utils import listen_http

if __name__ == "__main__":
    load_dotenv()

    listen_http()
    bot.run(os.environ["DISCORD_TOKEN"])
