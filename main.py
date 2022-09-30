from discord import Member, VoiceState, Message
from slash_functions import *


@bot.event
async def on_ready():
    global log_text_channel, afk_voice_channel, channel_members, admin_text_channel, channel, guild_synced
    logger.info(f"logged on as {bot.user}!")
    channel = bot.get_guild(channel_being_managed_id)
    if not guild_synced:
        await bot.tree.sync(guild=managed_guild_object)
        log_text_channel = await get_text_channel_by_name(log_text_channel_name)
        afk_voice_channel = await get_voice_channel_by_name(afk_voice_channel_name)
        admin_text_channel = await get_text_channel_by_name(admin_text_channel_name)
        await populate_channel_entity()
        await populate_members_structs()
        guild_synced = True
    logger.info(f"log text channel: {log_text_channel.name}")
    logger.info(f"afk voice channel: {afk_voice_channel.name}")
    logger.info(f"admin text channel: {admin_text_channel.name}")
    logger.info(f"afk timeout: {timeout_timer} seconds")
    logger.info(f"there are {len(channel_members)} members on '{channel.name}'")
    logger.info(
        "member dictionary populated: " + str(sorted(channel_members_names.items()))
    )
    logger.info(guild_synced)


@bot.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    global channel_members
    voice_state = member.voice
    if voice_state is not None:
        if voice_state.channel != afk_voice_channel:
            # TODO: enable users to avoid being moved to the AFK channel if they are streaming (voice_state.self_stream)
            # Maybe also make the same logic if they are with their webcam on (voice_state.self_video)
            if voice_state.self_deaf:
                member_early_interrupt = await countdown(member)
                if not member_early_interrupt:
                    await log_text_channel.send(
                        f"{member.mention} movido para o {afk_voice_channel.name}."
                    )
                    await member.move_to(afk_voice_channel)
            if before.self_deaf and not after.self_deaf:
                channel_members[member.name].timeout.interrupt_by_undeafen = True
        else:
            if channel_members[member.name].timeout.is_timing_out:
                channel_members[
                    member.name
                ].timeout.interrupt_by_afk_channel_move = True


@bot.event
async def on_member_join(member: Member):
    await populate_members_structs()


@bot.event
async def on_member_remove(member: Member):
    await populate_members_structs()


@bot.event
async def on_message(message: Message):
    if message.author != bot.user:  # not answering bot's own messages
        if not message.guild:  # DM messages
            await message.channel.send(
                "Por que está falando comigo, quer alguma coisa?"
            )


bot.run(token=discord_token, log_handler=None)
