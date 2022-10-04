from http.client import HTTPSConnection
from backoff import expo, on_exception
from table2ascii import table2ascii as t2a, PresetStyle
from asyncio import sleep
from discord import (
    ChannelType,
    Member,
)
from socket import gaierror
from aiohttp.client_exceptions import ClientConnectorError
from globals import *
from logger import *


@on_exception(
    wait_gen=expo,
    exception=(gaierror, ClientConnectorError),
    max_time=600,
    logger=logger,
)
def check_connection():
    connection = HTTPSConnection("discord.com", timeout=5)
    connection.request("HEAD", "/")
    connection.close()


async def countdown(member: Member):
    global channel_members
    channel_member = channel_members[member.name]
    early_interrupt = False
    end_string = f"countdown end for {channel_member.discord_entity.name}."
    if not channel_member.timeout.is_timing_out:
        step = 0.1
        channel_member.timeout.is_timing_out = True
        logger.info(f"countdown start for {channel_member.discord_entity.name}")
        while channel_member.timeout.timer > 0 and channel_member.timeout.is_timing_out:
            await sleep(step)
            channel_member.timeout.timer -= step
            if channel_member.timeout.interrupt_by_undeafen:
                early_interrupt = True
                end_string += " early interrupted by undeafen"
            elif channel_member.timeout.interrupt_by_afk_channel_move:
                early_interrupt = True
                end_string += " early interrupted by moving to AFK channel"
            elif channel_member.timeout.interrupt_by_self_disconnect:
                early_interrupt = True
                end_string += " early interrupted by self disconnecting"
            if early_interrupt:
                end_string += f" - time left: {channel_member.timeout.timer:.1f}"
                break
        logger.info(f"{end_string}")
    reload_user_entry(channel_member.discord_entity.name)
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
    global channel_members, channel_members_names, populate_members_called
    for member in channel.members:
        channel_members[member.name] = ChannelMember(member)
    for member in channel_members:
        if not channel_members[member].discord_entity.bot:
            channel_members_names[member] = channel_members[member].discord_entity.nick
    populate_members_called += 1
    logger.info(
        f"members struct populated! struct populated {populate_members_called} times since last initialization"
    )


def build_members_table():
    temp = dict(sorted(channel_members.items()))
    body = [
        (
            temp[member].discord_entity.name,
            temp[member].timeout.is_timing_out,
            (
                temp[member].timeout.interrupt_by_undeafen,
                temp[member].timeout.interrupt_by_afk_channel_move,
                temp[member].timeout._interrupt_by_self_disconnect,
            ),
            f"{temp[member].timeout.timer:.1f}",
        )
        for member in temp
        if not temp[member].discord_entity.bot
    ]
    output = t2a(
        header=[
            "Member",
            "Is timing out?",
            "undeafen | AFK | disconnect",
            "Countdown timer",
        ],
        body=body,
        style=PresetStyle.thin_compact,
    )
    return output


def reload_user_entry(channel_member_name: str):
    global channel_members
    channel_members[channel_member_name].timeout.is_timing_out = False
    channel_members[channel_member_name].timeout.interrupt_by_afk_channel_move = False
    channel_members[channel_member_name].timeout.interrupt_by_undeafen = False
    channel_members[channel_member_name].timeout.interrupt_by_self_disconnect = False
    channel_members[channel_member_name].timeout.timer = timeout_timer
