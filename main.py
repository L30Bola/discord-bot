from os import getenv
from asyncio import (
    sleep,
    create_task
)
from discord import (
    Client,
    Intents,
    ChannelType,
    Member,
    VoiceState
)

discord_token = getenv("DISCORD_TOKEN")

intents = Intents.default()
intents.message_content = True
intents.voice_states = True

client = Client(intents=intents)

channel_being_managed_id = int(getenv("CHANNEL_BEING_MANAGED_ID"))
log_text_channel_name = getenv("LOG_TEXT_CHANNEL_NAME")
log_text_channel = None
afk_voice_channel_name = getenv("AFK_VOICE_CHANNEL_NAME")
afk_voice_channel = None

channel_members = {}

async def countdown(time: float | int, member: Member):
    step = 0.1
    early_interrupt = False
    print(f"countdown start for {member.name}")
    while time > 0:
        await sleep(step)
        time -= step
        if channel_members[member.name]["timeout_interrupt"]:
            channel_members[member.name]["timeout_interrupt"] = False
            early_interrupt = True
            break
    print(f"countdown end for {member.name}. time left: {time:.1f}")
    return early_interrupt

async def get_text_channel_by_name(channel_name: str):
    current_guild = client.get_guild(channel_being_managed_id)
    channels = current_guild.channels
    for channel in channels:
        if channel.type == ChannelType.text:
            if channel.name == channel_name:
                return channel
    return None

async def get_voice_channel_by_name(channel_name: str):
    current_guild = client.get_guild(channel_being_managed_id)
    channels = current_guild.channels
    for channel in channels:
        if channel.type == ChannelType.voice:
            if channel.name == channel_name:
                return channel
    return None

@client.event
async def on_ready():
    print(f"logged on as {client.user}!")
    global log_text_channel, afk_voice_channel, channel_members
    log_text_channel = await get_text_channel_by_name(log_text_channel_name)
    afk_voice_channel = await get_voice_channel_by_name(afk_voice_channel_name)
    print(f"log text channel: {log_text_channel.name}")
    print(f"afk voice channel: {afk_voice_channel.name}")
    for member in client.get_guild(channel_being_managed_id).members:
        channel_members[member.name] = {
            "entity": member,
            "timeout_interrupt": None,
        }
    print("member dictionary populated")

@client.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    voice_state = member.voice
    if voice_state.channel != afk_voice_channel and voice_state is not None:
        if voice_state.self_deaf:
            task = create_task(countdown(30, member))
            member_early_interrupt = await task
            if not member_early_interrupt:
                await log_text_channel.send(f"{member.mention} movido para o {afk_voice_channel.name}.")
                await member.move_to(afk_voice_channel)
        if before.self_deaf and not after.self_deaf:
            channel_members[member.name]["timeout_interrupt"] = True

client.run(token=discord_token)