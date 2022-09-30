from helper_functions import *
from discord import Interaction


@bot.tree.command(
    name="print_members_timeout",
    description="Print the list of members struct",
    guild=managed_guild_object,
)
async def print_members_timeout(interaction: Interaction):
    output = build_members_table()
    if len(output) < 2001:
        await interaction.response.send_message(f"```\n{output}\n```", ephemeral=True)
    else:
        await interaction.response.defer(ephemeral=True)
        i = 0
        j = 0
        while i < len(output):  # TODO: this is a very poor way of spliting the string.
            # Embeds aren't good either, as their width is kinda shitty
            # Maybe the solution is creating an image for this output, kinda like IdleRPG Bot does
            i += 1992  # 2000 characters is the limit: 1992 characters + ```\n \n```
            await interaction.followup.send(f"```\n{output[j:i]}\n```", ephemeral=True)
            if i + 1992 > len(output):
                await interaction.followup.send(
                    f"```\n{output[i:len(output) + 1]}\n```", ephemeral=True
                )
                break
            else:
                j = i


@bot.tree.command(
    name="refresh",
    description="Refresh the members structs",
    guild=managed_guild_object,
)
async def refresh_members(interaction: Interaction):
    await interaction.response.send_message("Users structs refreshed!", ephemeral=True)
    await populate_members_structs()


@bot.tree.command(
    name="print_populate_members",
    description="Print how many times the populate_members_structs has been populated",
    guild=managed_guild_object,
)
async def print_populate_members(interaction: Interaction):
    global populate_members_called
    await interaction.response.send_message(populate_members_called, ephemeral=True)


@bot.tree.command(
    name="refresh_user",
    description="Reload the user entry on the channel_members struct",
    guild=managed_guild_object,
)
async def refresh_user(interaction: Interaction, name: str):
    channel = bot.get_guild(channel_being_managed_id)
    for m in channel.members:
        if m.id == int(name.strip("<").strip(">").strip("@")):
            member = m
    reload_user_entry(member.name)
    await interaction.response.send_message(
        f"{member.name} entry on members struct refreshed!", ephemeral=True
    )
