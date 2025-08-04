import discord
from discord.ext import commands
from main import get_bot

class bugReport(discord.ui.Modal, title='Bug Report'):
    guildid = discord.ui.TextInput(
        label='The ID of the guild where the bug took place',
        placeholder='e.g. 1300798921555054653',
        required=True,
        style=discord.TextStyle.short
    )
    bug = discord.ui.TextInput(
        label='Please describe the bug you encountered.',
        required=True,
        style=discord.TextStyle.long
    )

    async def on_submit(self, interaction: discord.Interaction):
        guild: discord.Guild = interaction._client.get_guild(1300798921555054653)
        channel = guild.get_channel(1400137514454355988)
        await channel.send(f'>>> # Bug Report Submitted!\n------------------------------------------\n## Guild ID:\n"{self.guildid.value}"\n\n## Bug Description:\n------------------------------------------\n"{self.bug.value}"\n-"{interaction.user.display_name}"')
        await interaction.response.send_message('Thank you for your bug report, you will get a message in your guild if the bot is updated!', ephemeral=True)
