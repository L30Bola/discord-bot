from discord import Intents, Game, Object, Guild
from discord.ext.commands import Bot
from channelmember import *

discord_token = getenv("DISCORD_TOKEN")

channel_being_managed_id = int(getenv("CHANNEL_BEING_MANAGED_ID"))

log_text_channel_name = getenv("LOG_TEXT_CHANNEL_NAME")
log_text_channel = None

afk_voice_channel_name = getenv("AFK_VOICE_CHANNEL_NAME")
afk_voice_channel = None

ignore_bot_users = getenv("IGNORE_BOT_USERS", "False")

channel: Guild = None
channel_members: dict[str, ChannelMember] = {}
channel_members_names: dict[str, str] = {}

intents = Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

activity = Game(name="Mantendo a ordem! Farmadores não passarão!!")
bot = Bot(
    intents=intents,
    activity=activity,
    command_prefix="#",
)

managed_guild_object = Object(id=channel_being_managed_id)
guild_synced = False
populate_members_called = 0
