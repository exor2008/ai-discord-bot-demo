import os

import openai
from dotenv import load_dotenv

from ai_discord_bot_demo.bot import bot

if __name__ == "__main__":
    load_dotenv()

    bot.run(os.environ["DISCORD_TOKEN"])
