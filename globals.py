from os import getenv
from discord import (
    Intents,
    Game
)
from discord.ext.commands import Bot

discord_token = getenv("DISCORD_TOKEN")

channel_being_managed_id = int(getenv("CHANNEL_BEING_MANAGED_ID"))
log_text_channel_name = getenv("LOG_TEXT_CHANNEL_NAME")
log_text_channel = None
afk_voice_channel_name = getenv("AFK_VOICE_CHANNEL_NAME")
afk_voice_channel = None
timeout_timer = int(getenv("TIMEOUT_TIMER"))

channel = None
channel_members = {}
channel_members_names = {}

intents = Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

activity = Game(name="Mantendo a ordem! Farmadores não passarão!!")
bot = Bot(
    intents=intents,
    activity=activity,
    command_prefix="#"
)
