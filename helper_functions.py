from table2ascii import table2ascii as t2a, PresetStyle
from asyncio import sleep
from discord import (
    ChannelType,
    Member,
    Embed
)
from globals import *
from logger import *

async def countdown(member: Member):
    channel_member = channel_members[member.name]
    early_interrupt = False
    end_string = f"countdown end for {channel_member.discord_entity.name}."
    if not channel_member.is_timing_out:
        step = 0.1
        channel_member.is_timing_out = True
        logger.info(f"countdown start for {channel_member.discord_entity.name}")
        while channel_member.timeout_timer > 0:
            await sleep(step)
            channel_member.timeout_timer -= step
            if channel_member.timeout_interrupt:
                early_interrupt = True
                end_string += f" early interrupted, time left: {channel_member.timeout_timer:.1f}"
                break
        logger.info(f"{end_string}")
    reload_user_entry(channel_member, channel_members)
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
        channel_members[member.name] = ChannelMember(member)
    for member in channel_members:
        if not channel_members[member].discord_entity.bot:
            channel_members_names[member] = channel_members[member].discord_entity.nick

def build_members_table(channel_members: dict[str, ChannelMember]):
    body = [(channel_members[member].discord_entity.name,channel_members[member].is_timing_out,channel_members[member].timeout_interrupt,f"{channel_members[member].timeout_timer:.1f}") for member in channel_members if not channel_members[member].discord_entity.bot]
    output = t2a(
        header = ["Member", "Is timing out?", "Timeout interrupt", "Countdown timer"],
        body = body,
        style = PresetStyle.thin_compact
    )
    return output

def reload_user_entry(channel_member: ChannelMember, channel_members: dict[str, ChannelMember]):
    channel_members[channel_member.discord_entity.name].is_timing_out = False
    channel_members[channel_member.discord_entity.name].timeout_interrupt = False
    channel_members[channel_member.discord_entity.name].timeout_timer = timeout_timer