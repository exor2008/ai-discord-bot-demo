import traceback

from interactions import (
    Embed,
    Extension,
    OptionType,
    SlashContext,
    slash_command,
    slash_option,
)
from interactions.ext.paginators import Paginator

from ai_discord_bot_demo.ai import Avatar, generate
from ai_discord_bot_demo.bot.chat import chat
from ai_discord_bot_demo.utils import logger

PAGINATION = 2000


class ChatCommands(Extension):
    @slash_command("say", description="Speak with the ChatGPT")
    @slash_option(
        "message",
        "Your message for ChatGPT",
        OptionType.STRING,
        required=True,
    )
    async def say(self, ctx: SlashContext, message: str):
        await ctx.defer()
        guild_id = ctx.guild_id.real if ctx.guild_id else 0

        resp = await chat.say(guild_id, message)
        if len(resp) > PAGINATION:
            paginator = Paginator.create_from_string(ctx.bot, resp, page_size=2000)
            await paginator.send(ctx)
        else:
            await ctx.respond(resp)

    @say.error
    async def say_error(self, e, *args, **kwargs):
        logger.error(f"Error in /say\nTrace: {traceback.format_exc()}")

    @slash_command("set_behaviour", description="Set bot's behaviour")
    @slash_option(
        "behaviour",
        "Bot behaviour",
        OptionType.STRING,
        required=True,
    )
    async def set_behaviour(self, ctx: SlashContext, behaviour: str):
        guild_id = ctx.guild_id.real if ctx.guild_id else 0
        await chat.set_behaviour(guild_id, behaviour)
        await ctx.respond(
            f"Behaviour of AI ChatBot changed to {behaviour}. Message history cleared."
        )

    @set_behaviour.error
    async def set_behaviour_error(self, e, *args, **kwargs):
        logger.error(f"Error in /set_behaviour\nTrace: {traceback.format_exc()}")

    @slash_command(
        name="avatar",
        description="Generate funny avatar according to the description",
    )
    @slash_option(
        "description",
        "Avatar description",
        OptionType.STRING,
        required=True,
    )
    async def avatar(self, ctx: SlashContext, description: str) -> None:
        """
        Generates an avatar based on a short description

        Arguments:
        - description (str): Short description of avatar. E.g. Ancient Greek sailor steering a ship.
        """
        await ctx.defer()
        avatar = await generate(description)
        embed = get_avatar_embed(avatar)

        await ctx.send(embed=embed)

    @avatar.error
    async def avatar_error(self, e, *args, **kwargs):
        logger.error(f"Error in /avatar\nTrace: {traceback.format_exc()}")


def get_avatar_embed(avatar: Avatar) -> Embed:
    embed = Embed()
    embed = embed.add_image(avatar.url)
    embed = embed.add_field(" ", avatar.slogan)
    embed.set_footer(text=avatar.user_descr)

    return embed


def setup(bot):
    ChatCommands(bot)
