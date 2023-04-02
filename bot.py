from os import getenv
from typing import List, Final
from asyncio import sleep

from dotenv import load_dotenv
from disnake import (
    Intents,
    Activity,
    Status,
    Role,
    Client,
    Message,
)

load_dotenv()

ROLE_ID_ALLOWED_TO_POST_IMAGES: Final[int] = 1089551412968566864
CHANNELS_IMAGE_PURGE_ACTIVE_IN: Final[List[int]] = [717872509139026021]

INTENTS: Final[Intents] = Intents(
    guild_messages=True,
    message_content=True,
)

client: Client = Client(
    intents=INTENTS,
    status=Status.dnd,
    activity=Activity(name=f"I'm open source! Check my bio :)", type=1),
)

@client.event
async def on_message(message: Message) -> None:
    if (
        message.author.bot == False
        and message.channel.id in CHANNELS_IMAGE_PURGE_ACTIVE_IN
        and len(message.attachments) > 0
        and len([
            role.id for role in message.author.roles 
            if role.id != ROLE_ID_ALLOWED_TO_POST_IMAGES
        ]) == 0
    ):
        await message.delete()
        alert: Message = await message.channel.send(f"{message.author.mention}, you can't post images in this channel until you are **Level 50**, sorry.")
        await sleep(5)
        await alert.delete()

client.run(getenv("DISCORD_BOT_TOKEN"))
