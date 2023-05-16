import os

from dotenv import load_dotenv

from discord_bot.bot import bot

if __name__ == "__main__":
    load_dotenv()

    bot.run(os.environ["DISCORD_TOKEN"])
