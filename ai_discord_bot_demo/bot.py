import os
import random
import traceback
import warnings
from collections import defaultdict
from typing import Tuple, cast

import discord
from discord.ext import commands

from ai_discord_bot_demo.ai import Avatar, dialog, generate
from ai_discord_bot_demo.utils import logger, logger_file

intents = discord.Intents.default()
intents.message_content = True


class AIBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = defaultdict(
            lambda: [{"role": "system", "content": os.environ["DEFAULT_AI_BEHAVIOUR"]}]
        )

    async def say(self, guild_id: int, txt: Tuple[str, ...]) -> str:
        messages = self.messages[guild_id]
        messages.append({"role": "user", "content": " ".join(txt)})
        resp = await dialog(messages)
        messages.append({"role": "assistant", "content": resp})
        return resp

    async def set_behaviour(self, guild_id: int, new_behaviour: str) -> None:
        self.messages[guild_id] = [{"role": "system", "content": new_behaviour}]


bot = AIBot(command_prefix="/", intents=intents)


@bot.event
async def on_ready() -> None:
    logger.critical(
        f"Logged in as {bot.user} (ID: {bot.user.id if bot.user else None})"
    )


@bot.event
async def on_member_join(member) -> None:
    await member.send(f"Hi {member.mention}, type /start to begin interaction.")


@bot.command()  # type: ignore
async def menu(ctx) -> None:
    """
    Show the graphical menu of the bot commands.
    """
    await ctx.send(view=MenuView())


@bot.command()  # type: ignore
async def say(ctx, *txt: str) -> None:
    """
    Speak with the bot.

    Arguments:
    - txt (str): Your statement in the dialogue with bot. E.g. How are yuo?
    """
    if guild := ctx.guild:
        logger_file.critical(
            f'USE OF /SAY: guild: {guild}, user:{ctx.author.name}, content: {" ".join(txt)}'
        )
        resp = await bot.say(guild.id, txt)

        await ctx.reply(resp)


@bot.command()  # type: ignore
async def avatar(ctx, *txt: str) -> None:
    """
    Generates an avatar based on a short description

    Arguments:
    - txt (str): Short description of avatar. E.g. Ancient Greek sailor steering a ship.
    """
    logger_file.critical(
        f'USE OF /AVATAR: guild: {ctx.guild if ctx.guild else None}, user:{ctx.author.name}, content: {" ".join(txt)}'
    )
    await ctx.defer()

    try:
        avatar = await generate(" ".join(txt))
    except Exception as e:
        warnings.warn(traceback.format_exc())
        await ctx.reply("Ooops... Something went wrong. Try again later.")
    else:
        embed = get_avatar_embed(avatar)

        await ctx.reply(embeds=[embed])


class MenuView(discord.ui.View):
    @discord.ui.select(
        placeholder="Choose option",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Adjust AI Chat",
                description="Generate a picture and description using OpenAI technologies.",
            ),
            discord.SelectOption(
                label="Generate avatar",
                description="Generate a picture and description using OpenAI technologies.",
            ),
        ],
    )
    async def select_callback(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ) -> None:
        if select.values[0] == "Adjust AI Chat":
            await interaction.response.send_modal(AIAdjustModal(title="Adjust AI Chat"))
        elif select.values[0] == "Generate avatar":
            await interaction.response.send_modal(
                AvatarDescrModal(title="Generate avatar")
            )


class AvatarDescrModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.TextInput(
                label="Avatar description.",
                style=discord.TextStyle.short,
                placeholder=random_avatar_example(),
            )
        )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=True)
        try:
            if value := getattr(self.children[0], "value"):
                logger_file.critical(
                    f"USE OF /AVATAR: guild: {interaction.guild if interaction.guild else None}, "
                    f"user:{interaction.user.name}, content: {value}"
                )
                avatar = await generate(value)
        except Exception as e:
            warnings.warn(traceback.format_exc())
            await interaction.followup.send(
                "Ooops... Something went wrong. Try again later."
            )
        else:
            embed = get_avatar_embed(avatar)

            await interaction.followup.send(embeds=[embed])


def get_avatar_embed(avatar: Avatar) -> discord.Embed:
    embed = discord.Embed(title=avatar.name)
    embed.set_image(url=avatar.url)
    embed.add_field(name=" ", value=avatar.slogan)
    embed.set_footer(text=avatar.user_descr)
    return embed


class AIAdjustModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.TextInput(
                label="Describe the desired behavior of AI ChatBot.",
                style=discord.TextStyle.short,
                placeholder=random_chat_behaviour(),
            )
        )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        if new_behaviour := getattr(self.children[0], "value"):
            client = interaction.client
            bot = cast(AIBot, client)
            if guild_id := getattr(interaction, "guild_id"):
                logger_file.critical(
                    f"USE OF /ADJ_BEHAV: guild: {interaction.guild if interaction.guild else None}, "
                    f"user:{interaction.user.name}, content: {new_behaviour}"
                )
                await bot.set_behaviour(guild_id, new_behaviour)
                await interaction.response.send_message(
                    f"Behaviour of AI ChatBot changed to {new_behaviour}. Message history cleared."
                )


def random_chat_behaviour() -> str:
    options = os.environ["AI_BEHAVIOURS"].split(", ")
    return random.choice(options)


def random_avatar_example() -> str:
    options = os.environ["AVATAR_EXAMPLES"].split(", ")
    return random.choice(options)
