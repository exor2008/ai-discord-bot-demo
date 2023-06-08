import os
import random
from enum import StrEnum

from interactions import (
    Client,
    ComponentCommand,
    ComponentContext,
    Extension,
    InputText,
    Modal,
    SlashContext,
    StringSelectMenu,
    TextStyles,
    slash_command,
)
from interactions.ext.paginators import Paginator

from ai_discord_bot_demo.ai import generate
from ai_discord_bot_demo.bot.chat import chat
from ai_discord_bot_demo.bot.commands import PAGINATION, get_avatar_embed


class MenuOptions(StrEnum):
    OPT_MAIN_MENU = "main_menu"
    OPT_ADJUST = "Adjust AI behaviour"
    OPT_AVATAR = "Generate avatar"
    OPT_SAY = "Speak with AI"


class ModalInputs(StrEnum):
    IN_ADJUST = "Input::adjust"
    IN_AVATAR = "Input::avatar"
    IN_SAY = "Input::say"


class ChatComponents(Extension):
    @slash_command("menu", description="Main menu")
    async def menu(self, ctx: SlashContext):
        await ctx.send("Select an iteration", components=get_main_menu())


async def on_menu(ctx: ComponentContext):
    match ctx.values[0]:
        case MenuOptions.OPT_ADJUST:
            modal = get_adjust_modal()
            await ctx.send_modal(modal=modal)
            modal_ctx = await ctx.bot.wait_for_modal(modal)
            new_behaviour = modal_ctx.responses[ModalInputs.IN_ADJUST]
            guild_id = ctx.guild_id.real if ctx.guild_id else 0
            await chat.set_behaviour(guild_id, new_behaviour)
            await modal_ctx.respond(f"AI Bot behaviour changed to <{new_behaviour}>")

        case MenuOptions.OPT_AVATAR:
            modal = get_avatar_modal()
            await ctx.send_modal(modal=modal)
            modal_ctx = await ctx.bot.wait_for_modal(modal)

            await modal_ctx.defer()
            avatar_descr = modal_ctx.responses[ModalInputs.IN_AVATAR]
            avatar = await generate(avatar_descr)
            embed = get_avatar_embed(avatar)
            await modal_ctx.respond(embed=embed)

        case MenuOptions.OPT_SAY:
            modal = get_say_modal()
            await ctx.send_modal(modal=modal)
            modal_ctx = await ctx.bot.wait_for_modal(modal)
            phrase = modal_ctx.responses[ModalInputs.IN_SAY]

            await modal_ctx.defer()
            guild_id = ctx.guild_id.real if ctx.guild_id else 0
            resp_phrase = await chat.say(guild_id, phrase)
            if len(resp_phrase) > PAGINATION:
                paginator = Paginator.create_from_string(
                    ctx.bot, resp_phrase, page_size=2000
                )
                await paginator.send(ctx)
            else:
                await modal_ctx.respond(resp_phrase)


def get_main_menu():
    return StringSelectMenu(
        MenuOptions.OPT_ADJUST,
        MenuOptions.OPT_AVATAR,
        MenuOptions.OPT_SAY,
        placeholder="Choose bot interaction",
        min_values=1,
        max_values=1,
        custom_id=MenuOptions.OPT_MAIN_MENU,
    )


def get_adjust_modal() -> Modal:
    return Modal(
        InputText(
            label="Describe the desired behavior of AI ChatBot.",
            style=TextStyles.SHORT,
            placeholder=random_chat_behaviour(),
            custom_id=ModalInputs.IN_ADJUST,
        ),
        title="Adjust AI behavior",
    )


def get_avatar_modal() -> Modal:
    return Modal(
        InputText(
            label="Describe the desired avatar.",
            style=TextStyles.SHORT,
            placeholder=random_avatar_example(),
            custom_id=ModalInputs.IN_AVATAR,
        ),
        title="Avatar creation",
    )


def get_say_modal() -> Modal:
    return Modal(
        InputText(
            label="Your phrase.",
            style=TextStyles.PARAGRAPH,
            placeholder=random_say_example(),
            custom_id=ModalInputs.IN_SAY,
        ),
        title="Speak with the bot",
    )


def random_chat_behaviour() -> str:
    options = os.environ["AI_BEHAVIOURS"].split(", ")
    return random.choice(options)


def random_avatar_example() -> str:
    options = os.environ["AVATAR_EXAMPLES"].split(", ")
    return random.choice(options)


def random_say_example() -> str:
    options = os.environ["SAY_EXAMPLES"].split(", ")
    return random.choice(options)


def setup(bot: Client):
    ChatComponents(bot)

    callback = ComponentCommand(
        name=f"ComponentCallback::{MenuOptions.OPT_MAIN_MENU}",
        callback=on_menu,
        listeners=[MenuOptions.OPT_MAIN_MENU],
    )
    bot.add_component_callback(callback)
