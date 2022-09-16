from asyncio import sleep
from discord import (
    ChannelType,
    Member,
)
from globals import *
from logger import *

async def countdown(time: float | int, member: Member):
    early_interrupt = False
    if not channel_members[member.name]["is_timing_out"]:
        step = 0.1
        channel_members[member.name]["is_timing_out"] = True
        logger.info(f"countdown start for {member.name}")
        while time > 0:
            await sleep(step)
            time -= step
            if channel_members[member.name]["timeout_interrupt"]:
                channel_members[member.name]["is_timing_out"] = False
                early_interrupt = True
                break
        logger.info(f"countdown end for {member.name}. time left: {time:.1f}")
    channel_members[member.name]["timeout_interrupt"] = False
    return early_interrupt

async def get_text_channel_by_name(channel_name: str):
    current_guild = bot.get_guild(channel_being_managed_id)
    channels = current_guild.channels
    for channel in channels:
        if channel.type == ChannelType.text:
            if channel.name == channel_name:
                return channel
    return None

async def get_voice_channel_by_name(channel_name: str):
    current_guild = bot.get_guild(channel_being_managed_id)
    channels = current_guild.channels
    for channel in channels:
        if channel.type == ChannelType.voice:
            if channel.name == channel_name:
                return channel
    return None

async def populate_channel_entity():
    global channel
    channel = bot.get_guild(channel_being_managed_id)

async def populate_members_structs():
    global channel_members, channel_members_names
    for member in channel.members:
        channel_members[member.name] = {
            "entity": member,
            "timeout_interrupt": False,
            "is_timing_out": False
        }
    for member in channel_members:
        if not channel_members[member]["entity"].bot:
            channel_members_names[member] = channel_members[member]["entity"].nick