import discord
import modals

class supportSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Support Server', emoji='⚙'),
            discord.SelectOption(label='Bot Info', emoji='ℹ'),
            discord.SelectOption(label='Bug Report', emoji='✉')
        ]
        super().__init__(placeholder='How can I help you today?', min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        selection = self.values[0].lower()
        if selection == 'support server':
            await interaction.response.send_message('You can get additional support at https://discord.gg/rdYDezfmwd', ephemeral=True)

        elif selection == 'bot info':
            await interaction.response.send_message(f'This currently doesn\'t work. Please don\'t bother making a bug report about it; I know about it, it\'s just that discord API is having some issues!', ephemeral=True)
        
        elif selection == 'bug report':
            await interaction.response.send_modal(modals.bugReport())

class supportView(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.add_item(supportSelect())