from helper_functions import *
from discord import (
    Interaction
)

@bot.tree.command(name="print_members_timeout", description="Print the list of members struct", guild=managed_guild_object)
async def print_members_timeout(interaction: Interaction):
    await interaction.response.send_message("Printing to terminal!")
    print(channel_members)