import os
from dataclasses import dataclass
from typing import Dict, List

import openai

openai.api_key = os.environ.get("OPENAI_KEY")


@dataclass
class Avatar:
    name: str
    url: str
    slogan: str
    user_descr: str


async def generate(task: str) -> Avatar:
    descr = await generate_description(task)
    name, slogan = descr.split("|")

    url = await generate_image(task)
    return Avatar(name, url, slogan, task)


async def generate_description(task: str) -> str:
    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": os.environ.get("GENERAL_TASK"),
            },
            {
                "role": "user",
                "content": task,
            },
        ],
    )

    return completion.get("choices")[0].get("message").get("content")


async def generate_image(descr: str) -> str:
    promt = os.environ["IMAGE_TASK"].format(descr=descr)
    response = await openai.Image.acreate(
        prompt=promt, n=1, size=os.environ.get("IMG_RES")
    )
    return response["data"][0]["url"]


async def dialog(messages: List[Dict[str, str]]) -> str:
    completion = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo", messages=messages
    )
    return completion.get("choices")[0].get("message").get("content")
