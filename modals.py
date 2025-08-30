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

class updateModal(discord.ui.Modal, title='Update'):
    updateVersion = discord.ui.TextInput(
        label='The version number of the new update',
        placeholder='V 1.0',
        required=True,
        style=discord.TextStyle.short
    )
    changeLog = discord.ui.TextInput(
        label='The changes made',
        required=False,
        style=discord.TextStyle.long
    )

    async def on_submit(self, interaction: discord.Interaction):
        guild: discord.Guild = interaction._client.get_guild(1298011793435656284)
        channel = guild.get_channel(1407764620483104950)
        if self.changeLog.value != '':
            changeLogs = self.changeLog.value
            await channel.send(f'>>> ### <:up:1411345083965640854> Dou Bot is Back! <:up:1411345083965640854>\n<:maintenance:1411345913258967041> Dou bot is now on version: "{self.updateVersion.value}"\n<:maintenance:1411345913258967041> These changes have now been made to Dou Bot\'s arsenal: \n"{changeLogs}"\n<:maintenance:1411345913258967041> Most importantly, Dou Bot is back online! Thank you for your patience!')
        else:
            await channel.send(f'>>> ### <:up:1411345083965640854> Dou Bot is Back! <:up:1411345083965640854>\n<:maintenance:1411345913258967041> Dou bot is now on version: "{self.updateVersion.value}"\n<:maintenance:1411345913258967041> No changes were specified for this update!\n<:maintenance:1411345913258967041> Most importantly, Dou Bot is back online! Thank you for your patience!')
        await interaction.response.send_message('Update sent!', ephemeral=True)