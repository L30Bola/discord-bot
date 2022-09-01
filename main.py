from os import getenv
from asyncio import sleep, create_task
from discord import Client, Intents, ChannelType, Member

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

async def countdown(time: float | int, member: Member):
    step = 0.1
    counter = 0
    print(f"countdown start for {member.name}")
    while time > 0:
        await sleep(step)
        time -= step
        counter += step
    print(f"countdown end for {member.name}")

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
    print(f'Logged on as {client.user}!')
    global log_text_channel, afk_voice_channel
    log_text_channel = await get_text_channel_by_name(log_text_channel_name)
    afk_voice_channel = await get_voice_channel_by_name(afk_voice_channel_name)
    print(f'log text channel: {log_text_channel.name}')
    print(f'afk voice channel: {afk_voice_channel.name}')

@client.event
async def on_voice_state_update(member, before, after):
    voice_state = member.voice
    if voice_state.channel != afk_voice_channel:
        # TODO: countdown should end if user re-enables it's audio (toggle deafen)
        # TODO: test if this works for multiples members at the same time
        if voice_state.self_deaf:
            task = create_task(countdown(10, member))
            await task
            # TODO: make the text message @mention the member being moved to afk channel
            await log_text_channel.send(f'{member.name} ({member.nick}) vai ser movido para o {afk_voice_channel.name}.')
            await member.move_to(afk_voice_channel)

client.run(token=discord_token)