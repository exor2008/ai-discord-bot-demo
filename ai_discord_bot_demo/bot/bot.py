from interactions import Client, Intents

from ai_discord_bot_demo.utils import logger

bot = Client(
    intents=Intents.DEFAULT | Intents.GUILD_MESSAGES,
    sync_interactions=True,
    asyncio_debug=True,
    logger=logger,
)


@bot.listen()
async def on_ready():
    logger.info(f"This bot is owned by {bot.owner}")


bot.load_extension("ai_discord_bot_demo.bot.commands")
bot.load_extension("ai_discord_bot_demo.bot.components")
