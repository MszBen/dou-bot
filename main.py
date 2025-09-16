import os, sys
from typing import Final, Optional
import discord
from discord import Intents, Message, app_commands
from discord.ext import commands
from dotenv import load_dotenv
import json
import selects
import datetime
import modals

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

basepath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

channelsFile = os.path.join(basepath, 'channels.json')
messagesFile = os.path.join(basepath, 'messages.json')
flaggedMessagesContentFile = os.path.join(basepath, 'flaggedmessages.json')
flaggedAuthorsIDFile = os.path.join(basepath, 'flaggedauthors.json')

logChannelID = 1407764620483104950
devID = 551056526777909259

intents: Intents = Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

controlGuildID = 1300798921555054653

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
    with open(flaggedMessagesContentFile, 'r') as f: # Load channels.json
        flaggedMessagesContents: list = json.load(f)
        f.close()
    with open(flaggedAuthorsIDFile, 'r') as f: # Load channels.json
        flaggedAuthorsIDs: list = json.load(f)
        f.close()
    
    for i in flaggedMessagesContents:
        content: str = i
        listContent: list = content.split('&')
        cleanedContent: str = listContent[0]
        if message.content == cleanedContent:
            logChannel = await message.guild.fetch_channel(logChannelID) # Gets the channel to put the logs into
            if listContent[1] == 'high':
                timeoutError = False
                deleteError = False
                try:
                    await message.author.timeout(datetime.timedelta(minutes=30))
                except:
                    timeoutError = True
                try:
                    await message.delete()
                except:
                    deleteError = True
                if timeoutError and deleteError:
                    await logChannel.send(f'Noticed message containing flagged content sent by user {message.author.mention} in channel {message.channel.mention} at {str(message.created_at)}. Attempted to timeout user and delete message, however both failed. This is probably because the user has higher permissions than the bot.\n-# If you think this is a mistake, please write a bug report using /support')
                    return
                elif timeoutError:
                    await logChannel.send(f'Noticed message containing flagged content sent by user {message.author.mention} in channel {message.channel.mention} at {str(message.created_at)}. Deleted message, however failed to timeout user. This is probably because the user has higher permissions than the bot.\n-# If you think this is a mistake, please write a bug report using /support')
                    return
                elif deleteError:
                    await logChannel.send(f'Noticed message containing flagged content sent by user {message.author.mention} in channel {message.channel.mention} at {str(message.created_at)}. Timed-out user, however failed to delete message. This is probably because the user has higher permissions than the bot.\n-# If you think this is a mistake, please write a bug report using /support')
                    return
                else:
                    await logChannel.send(f'Noticed message containing flagged content sent by user {message.author.mention} in channel {message.channel.mention} at {str(message.created_at)}. Timed-out user and deleted the message, as per flagging priority.\n-# If you think this is a mistake, please write a bug report using /support')
                    return
            elif listContent[1] == 'med' or listContent[1] == 'low':
                await logChannel.send(f'Noticed message containing flagged content sent by user {message.author.mention} in channel {message.channel.mention} at {str(message.created_at)}.\n-# If you think this is a mistake, please write a bug report using /support')
    
    for i in flaggedAuthorsIDs:
        content: str = i
        listContent: list = content.split('&')
        cleanedContent: int = int(listContent[0])
        if message.author.id == cleanedContent:
            logChannel = await message.guild.fetch_channel(logChannelID) # Gets the channel to put the logs into
            if listContent[1] == 'high':
                timeoutError = False
                deleteError = False
                try:
                    await message.author.timeout(datetime.timedelta(minutes=30))
                except:
                    timeoutError = True
                try:
                    await message.delete()
                except:
                    deleteError = True
                if timeoutError and deleteError:
                    await logChannel.send(f'Noticed message sent by flagged user {message.author.mention} in channel {message.channel.mention} at {str(message.created_at)}. Attempted to timeout user and delete message, however both failed. This is probably because the user has higher permissions than the bot.\n-# If you think this is a mistake, please write a bug report using /support')
                    return
                elif timeoutError:
                    await logChannel.send(f'Noticed message sent by flagged user {message.author.mention} in channel {message.channel.mention} at {str(message.created_at)}. Deleted message, however failed to timeout user. This is probably because the user has higher permissions than the bot.\n-# If you think this is a mistake, please write a bug report using /support')
                    return
                elif deleteError:
                    await logChannel.send(f'Noticed message sent by flagged user {message.author.mention} in channel {message.channel.mention} at {str(message.created_at)}. Timed-out user, however failed to delete message. This is probably because the user has higher permissions than the bot.\n-# If you think this is a mistake, please write a bug report using /support')
                    return
                else:
                    await logChannel.send(f'Noticed message sent by flagged user {message.author.mention} in channel {message.channel.mention} at {str(message.created_at)}. Timed-out user and deleted the message, as per flagging priority.\n-# If you think this is a mistake, please write a bug report using /support')
                    return
            elif listContent[1] == 'med' or listContent[1] == 'low':
                await logChannel.send(f'Noticed message sent by flagged user {message.author.mention} in channel {message.channel.mention} at {str(message.created_at)}.\n-# If you think this is a mistake, please write a bug report using /support')
    
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
    messageAuthors = []
    deleteError = False
    if len(susMessageChannelIDs) != 0: # If the list is not empty,
        for i in susMessageChannelIDs: # Removes duplicate channels from the list
            if susMessageChannelIDs.count(i) > 1:
                for b in range(susMessageChannelIDs.count(i) - 1):
                    susMessageChannelIDs.remove(i)
        for a in susMessageChannelIDs: # For all suspicous channel IDs,
            channel: discord.TextChannel = await message.guild.fetch_channel(int(a))
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
                    messageAuthors.append(messageToDelete.author)
                    if messageToDelete != None:
                        if messageToDelete.content != '' and messageToDelete.content != None:
                            await messageToDelete.delete()
                            if messageToDelete.author.is_timed_out() == False:
                                try:
                                    await messageToDelete.author.timeout(datetime.timedelta(1))
                                except:
                                    timeoutError = True
                                    timeoutErrorMessage = messageToDelete
                        else:
                            deleteError = True
                            break
                    else:
                        deleteError = True
                        break
                except:
                    deleteError = True
                    break
        if len(messageAuthors) != 0: # If the list is not empty,
            for i in messageAuthors: # Removes duplicate channels from the list
                if messageAuthors.count(i) > 1:
                    for b in range(messageAuthors.count(i) - 1):
                        messageAuthors.remove(i)
        
        authorNames = []
        authorMentions = []
        if len(messageAuthors) != 0:
            for i in messageAuthors:
                authorNames.append(i.name)
                authorMentions.append(i.mention)
        
        logChannel = await message.guild.fetch_channel(logChannelID) # Gets the channel to put the logs into
        if deleteError == True:
            if messageToDelete != None:
                dev = message.guild.get_member(devID)
                if dev != None:
                    dev.send('Tried and failed to delete messages')
                    return
                else:
                    dev = await message.guild.fetch_member(devID)
                    dev.send('Tried and failed to delete messages')
                    return
        cleaned = str(deletedMessages).strip('[').strip(']').replace("'", "") # Cleans the deleted messages list
        cleanedAuthorMentions = str(authorMentions).strip('[').strip(']').replace("'", "")
        cleanedAuthorNames = str(authorNames).strip('[').strip(']').replace("'", "")
        await logChannel.send(f'Deleted message(s) "{cleaned}" from user(s) "{cleanedAuthorMentions}" for reason: "Suspected Spam"\n-# If you think this is a mistake, please write a bug report using /support') # Creates a log for all deleted messages
        if timeoutError == True:
            await logChannel.send(f'Attempted to timeout "{timeoutErrorMessage.author.display_name}" ({timeoutErrorMessage.author.mention}) but failed. This could be due to insufficient permissions, or {timeoutErrorMessage.author.display_name} being higher ranked.\n-# If you think this is a mistake, please write a bug report using /support')
        dev = message.guild.get_member(devID)
        if dev != None:
            await dev.send(f'Deleted message(s) "{cleaned}" from user(s) "{cleanedAuthorNames}" for reason: "Suspected Spam"')
        else:
            dev = await message.guild.fetch_member(devID)
            await dev.send(f'Deleted message(s) "{cleaned}" from user(s) "{cleanedAuthorNames}" for reason: "Suspected Spam"')

@bot.event
async def on_ready():
    botName = bot.user.display_name
    botID = bot.user.id
    print(f'Logged in as {botName} ({botID})')
    print('----------------')
    try:
        # Sync global commands
        await bot.tree.sync()
        print("🌍 Synced global commands")

        # Sync guild-specific commands
        guild = discord.Object(id=controlGuildID)
        await bot.tree.sync(guild=guild)
        print(f"🏠 Synced guild commands to {controlGuildID}")
    except Exception as e:
        print("❌ Sync error:", e)

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

@bot.tree.command(name='maintenance', description='Announce maintenance', guild=discord.Object(id=controlGuildID))
async def maintenance(interaction: discord.Interaction):
    if interaction.user.id != devID:
        await interaction.response.send_message(f'{interaction.user.mention}, you do not have the correct permissions to use this command!\n-# Sorry!', ephemeral=True)
    else:
        channel = await interaction.client.fetch_channel(logChannelID)
        await channel.send(f'>>> ### <:undermaintenance:1411291719399510117> Dou Bot is Down For Maintenance <:undermaintenance:1411291719399510117>\n<:maintenance:1411345913258967041> Either for repair or a well deserved coffee break, the developer has taken this bot down temporarily but should be back up shortly!\n<:maintenance:1411345913258967041>We thank you for your patience!')
        await interaction.response.send_message('Message sent!',ephemeral=True)

@bot.tree.command(name='update', description='Announce an update', guild=discord.Object(id=controlGuildID))
async def update(interaction: discord.Interaction):
    if interaction.user.id != devID:
        await interaction.response.send_message(f'{interaction.user.mention}, you do not have the correct permissions to use this command!\n-# Sorry!', ephemeral=True)
    else:
        await interaction.response.send_modal(modals.updateModal())

@bot.tree.command(name='flagmessage',description='Flag a message as suspicous')
@app_commands.describe(level = 'Choose the priority level', messageid = 'Message ID to flag')
@app_commands.choices(level=[
    app_commands.Choice(name='High', value='high'),
    app_commands.Choice(name='Medium', value='med'),
    app_commands.Choice(name='Low', value='low')
])
async def flagchannel(interaction: discord.Interaction, level: app_commands.Choice[str], messageid: str):
    isadmin = False
    for i in interaction.user.roles:
        if i.permissions.administrator:
            isadmin = True
    if isadmin == False:
        await interaction.response.send_message(f'{interaction.user.mention}, you do not have the correct permissions to use this command!\n-# Sorry!', ephemeral=True)
        return
    else:
        await interaction.response.defer(ephemeral=True)
        message = None
        for i in interaction.guild.text_channels:
            try:
                message = await i.fetch_message(int(messageid))
            except:
                pass
        if message == None:
            await interaction.followup.send(f'No message with the ID provided was found. Ensure this bot has the correct permissions to do this action.\n-# If this error persists, please write a bug report using /support', ephemeral=True)
            return
        else:
            
            if str(level.value) == 'high':
                messageContent = message.content
                messageAuthorid = str(message.author.id)
                with open(flaggedMessagesContentFile, 'r') as f:
                    messageContentData: list = json.load(f)
                    f.close()
                with open(flaggedAuthorsIDFile, 'r') as f:
                    authorsIDData: list = json.load(f)
                    f.close()
                contentPresent: bool = False
                authorIDPresent: bool = False
                splitMessageContentData = []
                splitAuthorIDsData = []
                for i in messageContentData:
                    index: str = i
                    contentList = index.split('&')
                    actualContent = contentList[0]
                    splitMessageContentData.append(actualContent)
                for i in authorsIDData:
                    index: str = i
                    idList = index.split('&')
                    actualID = idList[0]
                    splitAuthorIDsData.append(actualID)
                if messageContent in splitMessageContentData:
                    contentPresent = True
                if messageAuthorid in splitAuthorIDsData:
                    authorIDPresent = True
                if contentPresent and authorIDPresent:
                    await interaction.followup.send(f'This user ({message.author.mention}) **and** message content have already been flagged before and actions should have been taken when this message was sent.\n-# If you think this is a mistake, please write a bug report using /support', ephemeral=True)
                elif contentPresent:
                    authorsIDData.append(f'{messageAuthorid}&high')
                    await interaction.followup.send(f'This message has had it\'s contents flagged already so no action was taken there. This user ({message.author.mention}) has been added to the flagged users database (use /info flagging to find out what that means).\n-# If you think this is a mistake, please write a bug report using /support', ephemeral=True)
                elif authorIDPresent:
                    messageContentData.append(f'{messageContent}&high')
                    await interaction.followup.send(f'This user ({message.author.mention}) has already been flagged so no action was taken there. This message\'s content has been added to the flagged messages database (use /info flagging to find out what that means).\n-# If you think this is a mistake, please write a bug report using /support', ephemeral=True)
                else:
                    authorsIDData.append(f'{messageAuthorid}&high')
                    messageContentData.append(f'{messageContent}&high')
                    await interaction.followup.send(f'This user ({message.author.mention}) and this messages\'s content has been added to the flagged users and flagged messages databases, respectively (use /info flagging to find out what that means).', ephemeral=True)
                with open(flaggedMessagesContentFile, 'w') as f:
                    json.dump(messageContentData, f)
                    f.close
                with open(flaggedAuthorsIDFile, 'w') as f:
                    json.dump(authorsIDData, f)
                    f.close
            
            elif str(level.value) == 'med':
                messageContent = message.content
                messageAuthorid = str(message.author.id)
                with open(flaggedMessagesContentFile, 'r') as f:
                    messageContentData: list = json.load(f)
                    f.close()
                with open(flaggedAuthorsIDFile, 'r') as f:
                    authorsIDData: list = json.load(f)
                    f.close()
                contentPresent: bool = False
                authorIDPresent: bool = False
                splitMessageContentData = []
                splitAuthorIDsData = []
                for i in messageContentData:
                    index: str = i
                    contentList = index.split('&')
                    actualContent = contentList[0]
                    splitMessageContentData.append(actualContent)
                for i in authorsIDData:
                    index: str = i
                    idList = index.split('&')
                    actualID = idList[0]
                    splitAuthorIDsData.append(actualID)
                if messageContent in splitMessageContentData:
                    contentPresent = True
                if messageAuthorid in splitAuthorIDsData:
                    authorIDPresent = True
                if contentPresent and authorIDPresent:
                    await interaction.followup.send(f'This user ({message.author.mention}) **and** message content have already been flagged before and actions should have been taken when this message was sent.\n-# If you think this is a mistake, please write a bug report using /support', ephemeral=True)
                elif contentPresent:
                    authorsIDData.append(f'{messageAuthorid}&med')
                    await interaction.followup.send(f'This message has had it\'s contents flagged already so no action was taken there. This user ({message.author.mention}) has been added to the flagged users database (use /info flagging to find out what that means).\n-# If you think this is a mistake, please write a bug report using /support', ephemeral=True)
                elif authorIDPresent:
                    messageContentData.append(f'{messageContent}&med')
                    await interaction.followup.send(f'This user ({message.author.mention}) has already been flagged so no action was taken there. This message\'s content has been added to the flagged messages database (use /info flagging to find out what that means).\n-# If you think this is a mistake, please write a bug report using /support', ephemeral=True)
                else:
                    authorsIDData.append(f'{messageAuthorid}&med')
                    messageContentData.append(f'{messageContent}&med')
                    await interaction.followup.send(f'This user ({message.author.mention}) and this messages\'s content has been added to the flagged users and flagged messages databases, respectively (use /info flagging to find out what that means).', ephemeral=True)
                with open(flaggedMessagesContentFile, 'w') as f:
                    json.dump(messageContentData, f)
                    f.close
                with open(flaggedAuthorsIDFile, 'w') as f:
                    json.dump(authorsIDData, f)
                    f.close
            
            elif str(level.value) == 'low':
                messageContent = message.content
                with open(flaggedMessagesContentFile, 'r') as f:
                    messageContentData: list = json.load(f)
                    f.close()
                contentPresent: bool = False
                splitMessageContentData = []
                for i in messageContentData:
                    index: str = i
                    contentList = index.split('&')
                    actualContent = contentList[0]
                    splitMessageContentData.append(actualContent)
                if messageContent in splitMessageContentData:
                    contentPresent = True
                if contentPresent:
                    await interaction.followup.send(f'This message has had it\'s contents flagged already so no action was taken.\n-# If you think this is a mistake, please write a bug report using /support', ephemeral=True)
                else:
                    messageContentData.append(f'{messageContent}&low')
                    await interaction.followup.send(f'This messages\'s content has been added to the flagged messages database (use /info flagging to find out what that means).', ephemeral=True)
                with open(flaggedMessagesContentFile, 'w') as f:
                    json.dump(messageContentData, f)
                    f.close
            else:
                await interaction.followup.send(f'Hmmm, something didn\'t work. Please ensure you chose a correct option.\n-# If this error persists, please write a bug report using /support', ephemeral=True)

@bot.tree.command(name='info', description='Access the documentation for this bot')
@app_commands.describe(feature = 'Which feature do you require?')
@app_commands.choices(feature=[
    app_commands.Choice(name='flagging', value='flagging')
])
async def info(interaction: discord.Interaction, feature: app_commands.Choice[str]):
    if str(feature.value) == 'flagging':
        line = f'~~‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ~~'
        highprior = f'`•` High Priority *-* Adds user and message content to databases. Upon *any* user sending a message with the same message content as a message flagged with high priority, the message will be deleted, the user will be timed-out and a message will be sent notifying moderators. Upon a user flagged with high priority sending a message, the message will be deleted, the user will be timed-out and a message will be sent notifying moderators.'
        medprior = f'`•` Medium Priority *-* Adds user and message content to databases. Upon *any* user sending a message with the same message content as a message flagged with medium priority, a message will be sent notifying moderators. Upon a user flagged with medium priority sending a message, a message will be sent notifying moderators.'
        lowprior = f'`•` Low Priority *-* Adds message content to database. Upon *any* user sending a message with the same message content as a message flagged with low priority, a message will be sent notifying moderators.'
        embed = discord.Embed(title='Flagging', description=f'{line}\n**Flagging Priorities**\n{line}\n{highprior}\n\n{medprior}\n\n{lowprior}', color=discord.Color.blurple())
        embed.set_author(name='Ben MS', url='https://discord.com/users/551056526777909259', icon_url='https://cdn.discordapp.com/avatars/551056526777909259/cf6026a863922f21d0e76bc304c88933?size=1024')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(f'Hmmm, something didn\'t work. Please ensure you chose a correct option.\n-# If this error persists, please write a bug report using /support', ephemeral=True)

@bot.tree.command(name='flaggedusers', description='Edit the flagged users list')
@app_commands.describe(method = 'How do you want to edit this list?', user = 'Which user? (optional)')
@app_commands.choices(method=[
    app_commands.Choice(name='Clear', value='clr'),
    app_commands.Choice(name='Remove', value='rmve'),
    app_commands.Choice(name='List', value='ls')
])
async def flaggedusers(interaction: discord.Interaction, user: Optional[discord.Member], method: app_commands.Choice[str]):
    isadmin = False
    for i in interaction.user.roles:
        if i.permissions.administrator:
            isadmin = True
    if isadmin == False:
        await interaction.response.send_message(f'{interaction.user.mention}, you do not have the correct permissions to use this command!\n-# Sorry!', ephemeral=True)
        return
    else:
        await interaction.response.defer(ephemeral=True)
        if method.value == 'clr':
            clearedList = []
            with open(flaggedAuthorsIDFile, 'w') as f:
                json.dump(clearedList, f)
                f.close
            await interaction.followup.send(f'Flagged users database cleared!\n-# If you think this is a mistake, please write a bug report using /support', ephemeral=True)
        elif method.value == 'rmve':
            userID = str(user.id)
            with open(flaggedAuthorsIDFile, 'r') as f:
                authorsIDData: list = json.load(f)
                f.close()
            splitAuthorIDsData = []
            for i in authorsIDData:
                index: str = i
                idList = index.split('&')
                actualID = idList[0]
                splitAuthorIDsData.append(actualID)
            if len(splitAuthorIDsData) == 0:
                await interaction.followup.send(f'There are no users on the flagged users list, meaning there is no one to remove!\n-# If you think this is a mistake, please write a bug report using /support')
                return
            
            if userID not in splitAuthorIDsData:
                await interaction.followup.send(f'The user specified is not on the flagged user list.\n-# If you think this is a mistake, please write a bug report using /support', ephemeral=True)
            else:
                newList = []
                for i in authorsIDData:
                    index: str = i
                    idList = index.split('&')
                    actualID = idList[0]
                    if actualID != userID:
                        newList.append(i)
                with open(flaggedAuthorsIDFile, 'w') as f:
                    json.dump(newList, f)
                    f.close
                await interaction.followup.send(f'{user.mention} has been removed from the flagged users list!', ephemeral=True)
        elif method.value == 'ls':
            with open(flaggedAuthorsIDFile, 'r') as f:
                authorsIDData: list = json.load(f)
                f.close()
            splitAuthorIDsData = []
            for i in authorsIDData:
                index: str = i
                idList = index.split('&')
                actualID = idList[0]
                splitAuthorIDsData.append(actualID)
            if len(splitAuthorIDsData) != 0:
                cleaned = str(splitAuthorIDsData).strip('[').strip(']').replace("'", "")
                await interaction.followup.send(f'The flagged users database contains these IDs: "{cleaned}"', ephemeral=True)
            else:
                await interaction.followup.send(f'There are no flagged users in the database at the moment!', ephemeral=True)

@bot.tree.command(name='flaggedmessages', description='Edit the flagged messages list')
@app_commands.describe(method = 'How do you want to edit this list?', msgcontent = 'What content? (optional)')
@app_commands.choices(method=[
    app_commands.Choice(name='Clear', value='clr'),
    app_commands.Choice(name='Remove', value='rmve'),
    app_commands.Choice(name='List', value='ls')
])
async def flaggedmessages(interaction: discord.Interaction, msgcontent: Optional[str], method: app_commands.Choice[str]):
    isadmin = False
    for i in interaction.user.roles:
        if i.permissions.administrator:
            isadmin = True
    if isadmin == False:
        await interaction.response.send_message(f'{interaction.user.mention}, you do not have the correct permissions to use this command!\n-# Sorry!', ephemeral=True)
        return
    else:
        await interaction.response.defer(ephemeral=True)
        if method.value == 'clr':
            clearedList = []
            with open(flaggedMessagesContentFile, 'w') as f:
                json.dump(clearedList, f)
                f.close
            await interaction.followup.send(f'Flagged messages database cleared!\n-# If you think this is a mistake, please write a bug report using /support', ephemeral=True)
        elif method.value == 'rmve':
            with open(flaggedMessagesContentFile, 'r') as f:
                messagesContentData: list = json.load(f)
                f.close()
            splitMessageContentData = []
            for i in messagesContentData:
                index: str = i
                idList = index.split('&')
                actualContent = idList[0]
                splitMessageContentData.append(actualContent)
            if len(splitMessageContentData) == 0:
                await interaction.followup.send(f'There are no messages on the flagged messages list, meaning there is no one to remove!\n-# If you think this is a mistake, please write a bug report using /support')
                return
            
            if msgcontent not in splitMessageContentData:
                await interaction.followup.send(f'The message specified is not on the flagged messages list.\n-# If you think this is a mistake, please write a bug report using /support', ephemeral=True)
            else:
                newList = []
                for i in messagesContentData:
                    index: str = i
                    idList = index.split('&')
                    actualContent = idList[0]
                    if actualContent != msgcontent:
                        newList.append(i)
                with open(flaggedMessagesContentFile, 'w') as f:
                    json.dump(newList, f)
                    f.close
                await interaction.followup.send(f'Message "*{msgcontent}*" has been removed from the flagged users list!', ephemeral=True)
        elif method.value == 'ls':
            with open(flaggedMessagesContentFile, 'r') as f:
                messagesContentData: list = json.load(f)
                f.close()
            splitMessageContentData = []
            for i in messagesContentData:
                index: str = i
                idList = index.split('&')
                actualContent = idList[0]
                splitMessageContentData.append(actualContent)
            if len(splitMessageContentData) != 0:
                cleaned = str(splitMessageContentData).strip('[').strip(']').replace("'", "")
                await interaction.followup.send(f'The flagged messages database contains these contents: "{cleaned}"', ephemeral=True)
            else:
                await interaction.followup.send(f'There are no flagged messages in the database at the moment!', ephemeral=True)


def main() -> None:
    bot.run(TOKEN)

if __name__ == '__main__':
    main()