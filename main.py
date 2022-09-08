from discord import (
    Member,
    VoiceState, 
    Message
)
from helper_functions import *

@client.event
async def on_ready():
    logger.info(f"logged on as {client.user}!")
    global log_text_channel, afk_voice_channel, channel_members
    log_text_channel = await get_text_channel_by_name(log_text_channel_name)
    afk_voice_channel = await get_voice_channel_by_name(afk_voice_channel_name)
    logger.info(f"log text channel: {log_text_channel.name}")
    logger.info(f"afk voice channel: {afk_voice_channel.name}")
    channel = client.get_guild(channel_being_managed_id)
    await populate_channel_entity()
    await populate_members_structs()
    logger.info(f"there are {len(channel_members)} members on '{channel.name}'")
    logger.info("member dictionary populated: " + str(sorted(channel_members_names.items())))

@client.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    voice_state = member.voice
    if voice_state is not None:
        if voice_state.channel != afk_voice_channel:
        # TODO: enable users to avoid being moved to the AFK channel if they are streaming (voice_state.self_stream). 
        # Maybe also make the same logic if they are with their webcam on (voice_state.self_video)
            if voice_state.self_deaf:
                member_early_interrupt = await countdown(timeout_timer, member)
                if not member_early_interrupt:
                    await log_text_channel.send(f"{member.mention} movido para o {afk_voice_channel.name}.")
                    await member.move_to(afk_voice_channel)
            if before.self_deaf and not after.self_deaf:
                channel_members[member.name]["timeout_interrupt"] = True
            

@client.event
async def on_member_join(member: Member):
    await populate_members_structs()

@client.event
async def on_member_remove(member: Member):
    await populate_members_structs()

@client.event
async def on_message(message: Message):
    if message.channel.id == message.author.dm_channel.id: # DM messages
        await message.channel.send("Por que está falando comigo, quer alguma coisa?")

client.run(token=discord_token, log_handler=None)