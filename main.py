import os, sys
from typing import Final, Optional
import discord
from discord import Intents, Message, app_commands
from discord.ext import commands
from dotenv import load_dotenv
import json
import selects
import datetime

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

basepath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

channelsFile = os.path.join(basepath, 'channels.json')
messagesFile = os.path.join(basepath, 'messages.json')

logChannelID = 1407764620483104950
devID = 551056526777909259

intents: Intents = Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

def get_bot():
    return commands.Bot(command_prefix='!', intents=intents)

async def checkMessage(message: Message, messageContent: str): # Check whether messages are suspicous
    if message.author == bot.user: # If the message was sent by the bot itself, then ignores it.
        return
    if not messageContent: # If the message was empty (probably due to a bug) then return the string "none"
        return 'none'
    with open(messagesFile, 'r') as f: # Load messages.json
        messagesData: list = json.load(f)
        f.close()
    with open(channelsFile, 'r') as f: # Load channels.json
        channelsData: list = json.load(f)
        f.close()
    
    messagesData = [entry for entry in messagesData if entry['channelID'] in channelsData]

    loggedChannels: list = []
    for a in channelsData: # For all IDs in channels.json,
        if a.isalnum(): # If the ID is all numbers,
            for b in messagesData: # For all channels in messages.json,
                if a == b['channelID']: # If the ID from channels.json is the same as the channel ID from messages.json,
                    loggedChannels.append(a) # Add the ID to the loggedChannels lsit
    baseChannels: list = channelsData 
    for i in loggedChannels: # Removes all channel IDs which are logged in messages.json from the ones in channels.json to which have not been logged yet
        baseChannels.remove(i)
    remainingChannels: list = baseChannels
    data = []
    for i in remainingChannels: # For all channels that have not been logged yet,
        data.append({
            'channelID': f'{i}',
            'message1content': 'none',
            'message1id': 'none',
            'message2content': 'none',
            'message2id': 'none',
            'message3content': 'none',
            'message3id': 'none'
        }) # Adds the empty dictionary to the data list
    for i in messagesData: # For channels in messages.json,
        if i['channelID'] == str(message.channel.id): # If the channel ID is the same as the message's channel ID,
            if i['message1content'] != 'none': # If there is nothing logged for the first message,
                if i['message2content'] != 'none': # If there is nothing logged for the second message,
                    if i['message3content'] != 'none': # If there is nothing logged for the third message,
                        data.append({
                            'channelID': f'{message.channel.id}',
                            'message1content': f'{messageContent}',
                            'message1id': f'{message.id}',
                            'message2content': f'{i["message1content"]}',
                            'message2id': f'{i["message1id"]}',
                            'message3content': f'{i["message2content"]}',
                            'message3id': f'{i["message2id"]}'
                        }) # Adds the corresponding dictionary to the data list
                    else:
                        data.append({
                            'channelID': f'{message.channel.id}',
                            'message1content': f'{i["message1content"]}',
                            'message1id': f'{i["message1id"]}',
                            'message2content': f'{i["message2content"]}',
                            'message2id': f'{i["message2id"]}',
                            'message3content': f'{messageContent}',
                            'message3id': f'{message.id}'
                        }) # Adds the corresponding dictionary to the data list
                else:
                    data.append({
                        'channelID': f'{message.channel.id}',
                        'message1content': f'{i["message1content"]}',
                        'message1id': f'{i["message1id"]}',
                        'message2content': f'{messageContent}',
                        'message2id': f'{message.id}',
                        'message3content': 'none',
                        'message3id': 'none'
                    }) # Adds the corresponding dictionary to the data list
            else:
                data.append({
                    'channelID': f'{message.channel.id}',
                    'message1content': f'{messageContent}',
                    'message1id': f'{message.id}',
                    'message2content': 'none',
                    'message2id': 'none',
                    'message3content': 'none',
                    'message3id': 'none'
                }) # Adds the corresponding dictionary to the data list
        else: # If it is not the same channel ID as the message's channel ID,
            data.append({
                'channelID': f'{i["channelID"]}',
                'message1content': f'{i["message1content"]}',
                'message1id': f'{i["message1id"]}',
                'message2content': f'{i["message2content"]}',
                'message2id': f'{i["message2id"]}',
                'message3content': f'{i["message3content"]}',
                'message3id': f'{i["message3id"]}'
            }) # Adds the channels original information to the data list
    if len(data) != 0: # If the data list is not empty,
        with open(messagesFile, 'w') as f:
            json.dump(data, f) # Dump the data list into the messages.json folder
            f.close()
    with open(messagesFile, 'r') as f:
        messagesData = json.load(f) # Load messages.json
        f.close()
    susMessageIDs = []
    susMessageChannelIDs = []
    allMessages = []
    for i in messagesData: # Goes through all logged messages for all logged channels and adds them to the allMessages list
        if i['message1content'] != 'none':
            allMessages.append(i['message1content'])
        if i['message2content'] != 'none':
            allMessages.append(i['message2content'])
        if i['message3content'] != 'none':
            allMessages.append(i['message3content'])
    for i in messagesData: # For all logged channels, if any messages is in the allMessages list more than twice, it is added to the suspicious messages list, along with its channel ID
        if allMessages.count(i['message1content']) > 2:
            susMessageIDs.append(i['message1id'])
            susMessageChannelIDs.append(i['channelID'])
        if allMessages.count(i['message2content']) > 2:
            susMessageIDs.append(i['message2id'])
            susMessageChannelIDs.append(i['channelID'])
        if allMessages.count(i['message3content']) > 2:
            susMessageIDs.append(i['message3id'])
            susMessageChannelIDs.append(i['channelID'])
    
    deletedMessages = []
    timeoutError = False
    timeoutErrorMessage = None
    if len(susMessageChannelIDs) != 0: # If the list is not empty,
        for i in susMessageChannelIDs: # Removes duplicate channels from the list
            if susMessageChannelIDs.count(i) > 1:
                for b in range(susMessageChannelIDs.count(i) - 1):
                    susMessageChannelIDs.remove(i)
        for a in susMessageChannelIDs: # For all suspicous channel IDs,
            channel: discord.TextChannel = message.guild.get_channel(int(a))
            if channel == None: # If the channel is not found, then return "channel error"
                print('-------------------')
                print('Channel was None again for some reason.')
                print(f'Channel: {channel} Date: {datetime.datetime.now()}')
                print(f'Current message content: {message.content}')
                return 'channel error'
            for b in susMessageIDs: #Goes through all suspicous messages and deletes them if they are in the current channel
                try:
                    messageToDelete: Message = await channel.fetch_message(b)
                    deletedMessages.append(f'{messageToDelete.content}')
                    await messageToDelete.delete()
                    if messageToDelete.author.is_timed_out() == False:
                        try:
                            await messageToDelete.author.timeout(datetime.timedelta(1))
                        except:
                            timeoutError = True
                            timeoutErrorMessage = messageToDelete
                except:
                    pass
        logChannel = message.guild.get_channel(logChannelID) # Gets the channel to put the logs into
        cleaned = str(deletedMessages).strip('[').strip(']').replace("'", "") # Cleans the deleted messages list
        await logChannel.send(f'Deleted message(s) "{cleaned}" for reason: "Suspected Spam"\n-# If you think this is a mistake, please write a bug report using /support') # Creates a log for all deleted messages
        if timeoutError == True:
            await logChannel.send(f'Attempted to timeout "{timeoutErrorMessage.author.display_name}" ({timeoutErrorMessage.author.mention}) but failed. This could be due to insufficient permissions, or {timeoutErrorMessage.author.display_name} being higher ranked.\n-# If you think this is a mistake, please write a bug report using /support')
        dev = message.guild.get_member(devID)
        if dev != None:
            await dev.send(f'Deleted message(s) "{cleaned}" for reason: "Suspected Spam"')
        else:
            dev = await message.guild.fetch_member(devID)
            await dev.send(f'Deleted message(s) "{cleaned}" for reason: "Suspected Spam"')

@bot.event
async def on_ready():
    botName = bot.user.display_name
    botID = bot.user.id
    print(f'Logged in as {botName} ({botID})')
    print('----------------')
    synced = await bot.tree.sync()
    print(f'Synced {len(synced)} command(s)')

@bot.tree.command(name='support', description='Get support or report a bug')
async def support(interaction: discord.Interaction):
    isadmin = False
    for i in interaction.user.roles:
        if i.permissions.administrator:
            isadmin = True
    if isadmin == False:
        await interaction.response.send_message(f'{interaction.user.mention}, if you need support, please contact an admin!', ephemeral=True)
        return
    else:
        await interaction.response.send_message(f'>>> Hello, {interaction.user.mention}!', view=selects.supportView(),ephemeral=True)

@bot.event
async def on_message(message: Message) -> None:
    messageContent = message.content
    check = await checkMessage(message, messageContent)
    if check == 'none':
        print('Message was empty. Check intents.')
        return
    if check == 'channel error':
        print('Channel was not found.')
        print('-------------------')
        return



@bot.tree.command(name='addchannel', description='Add a channel to anti-raiding')
@app_commands.describe(channel = 'Pick a channel to add')
async def addchannel(interaction: discord.Interaction, channel: discord.TextChannel):
    isadmin = False
    for i in interaction.user.roles:
        if i.permissions.administrator:
            isadmin = True
    if isadmin == False:
        await interaction.response.send_message(f'{interaction.user.mention}, you do not have the correct permissions to use this command!\n-# Sorry!', ephemeral=True)
        return
    else:
        with open(channelsFile, 'r') as f:
            channelsData: list = json.load(f)
            f.close()
        if str(channel.id) not in channelsData:
            channelsData.append(str(channel.id))
            with open(channelsFile, 'w') as f:
                json.dump(channelsData, f)
                f.close
                await interaction.response.send_message(f'{channel.mention} was added to the protected channel list!', ephemeral=True)
                if interaction.user.id != 551056526777909259:
                    logChannel = await interaction.client.fetch_channel(logChannelID)
                    await logChannel.send(f'"{interaction.user.mention}" added "{channel.mention}" to the protected channel list!\n-# If this was a mistake, you can use /removechannel to undo this action.')
        else:
            await interaction.response.send_message(f'{channel.mention} is already in the protected server list!', ephemeral=True)

@bot.tree.command(name='removechannel', description='Remove a channel from anti-raiding')
@app_commands.describe(channel = 'Pick a channel to remove')
async def removechannel(interaction: discord.Interaction, channel: discord.TextChannel):
    isadmin = False
    for i in interaction.user.roles:
        if i.permissions.administrator:
            isadmin = True
    if isadmin == False:
        await interaction.response.send_message(f'{interaction.user.mention}, you do not have the correct permissions to use this command!\n-# Sorry!', ephemeral=True)
        return
    else:
        with open(channelsFile, 'r') as f:
            channelsData: list = json.load(f)
            f.close()
        if str(channel.id) in channelsData:
            channelsData.remove(f'{channel.id}')
            with open(channelsFile, 'w') as f:
                json.dump(channelsData, f)
                f.close
                await interaction.response.send_message(f'{channel.mention} was removed from the protected channel list!', ephemeral=True)
                if interaction.user.id != 551056526777909259:
                    logChannel = await interaction.client.fetch_channel(logChannelID)
                    await logChannel.send(f'"{interaction.user.mention}" removed "{channel.mention}" from the protected channel list!\n-# If this was a mistake, you can use /removechannel to undo this action.')
        else:
            await interaction.response.send_message(f'{channel.mention} is not in the protected server list!', ephemeral=True)

@bot.tree.command(name='protchannels', description='Lists all protected channels')
async def protchannels(interaction: discord.Interaction):
    isadmin = False
    for i in interaction.user.roles:
        if i.permissions.administrator:
            isadmin = True
    if isadmin == False:
        await interaction.response.send_message(f'{interaction.user.mention}, you do not have the correct permissions to use this command!\n-# Sorry!', ephemeral=True)
        return
    else:
        with open(channelsFile, 'r') as f:
            channelsData: list = json.load(f)
            f.close()
        guildProtChannels = []
        for i in channelsData:
            channel = await interaction.client.fetch_channel(i)
            if channel != None:
                guildProtChannels.append(channel.name)
        cleaned = str(guildProtChannels).strip('[').strip(']').replace("'", "")
        await interaction.response.send_message(f'All protected channels (in this guild): {cleaned}', ephemeral=True)

@bot.tree.command(name='socials', description='Get all socials of Douthepuppy')
async def socials(interaction: discord.Interaction):
    embeds = []
    twitchEmbed = discord.Embed(title='* Twitch *', description='Musician turned streamer -18, UK, Mostly play horror games and Shooters (Eg, The Forest Franchise, Marvel Rivals, Valorant, Roblox, etc.)', color=discord.Color.from_rgb(90, 62, 133), timestamp=datetime.datetime(2025, 8, 6, 15, 16))
    twitchEmbed.set_footer(text='This is up-to-date as of:')
    twitchEmbed.add_field(name=' ', value='You can visit Douthepuppy\'s Twitch channel [here](https://www.twitch.tv/douthepuppy).')
    twitchEmbed.set_thumbnail(url='https://images.seeklogo.com/logo-png/27/2/twitch-logo-png_seeklogo-274042.png')
    embeds.append(twitchEmbed)
    YTEmbed = discord.Embed(title='* YouTube *', description='Guitarist and no life for practically any game', color=discord.Color.from_rgb(255, 0, 0), timestamp=datetime.datetime(2025, 8, 6, 15, 16))
    YTEmbed.set_footer(text='This is up-to-date as of:')
    YTEmbed.add_field(name=' ', value='You can visit Douthepuppy\'s YouTube channel [here](https://www.youtube.com/@douthepuppy).')
    YTEmbed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/commons/e/ef/Youtube_logo.png')
    embeds.append(YTEmbed)
    await interaction.response.send_message(embeds=embeds, ephemeral=True)

def main() -> None:
    bot.run(TOKEN)

if __name__ == '__main__':
    main()