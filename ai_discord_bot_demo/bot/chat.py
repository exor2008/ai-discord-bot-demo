import os
from collections import defaultdict

from ai_discord_bot_demo.ai import dialog


class Chat:
    def __init__(self) -> None:
        self.messages = defaultdict(
            lambda: [{"role": "system", "content": os.environ["DEFAULT_AI_BEHAVIOUR"]}]
        )

    async def say(self, guild_id: int, txt: str) -> str:
        messages = self.messages[guild_id]
        messages.append({"role": "user", "content": txt})
        resp = await dialog(messages)
        messages.append({"role": "assistant", "content": resp})
        return resp

    async def set_behaviour(self, guild_id: int, new_behaviour: str) -> None:
        self.messages[guild_id] = [{"role": "system", "content": new_behaviour}]


chat = Chat()
