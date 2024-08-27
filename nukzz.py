import discord
from discord.ext import commands
import aiohttp
import random
import logging
import asyncio
import os
from datetime import datetime

# Logging-Konfiguration: Fehler und kritische Logs aktivieren
logging.basicConfig(level=logging.ERROR)

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

# Asynchrone Menüfunktion
async def menu():
    while True:
        print("\033[92m" + """
┌─────────────────────────────────────────────────────────┐
│ [ 1] Create and Delete Channels       │ [12] Show All Roles      │
│ [ 2] Rename Server                    │ [13] Server Settings     │
│ [ 3] Mass Create Threads              │ [14] Change Channel Description │
│ [ 4] Webhook Spammer                  │ [15] Remove Bots         │
│ [ 5] Delete Webhook                   │ [16] Delete Server       │
│ [ 6] Delete All Webhooks              │ [17] Spam Channels       │
│ [ 7] Server Info                      │ [18] Notify All Members  │
│ [ 8] Rename All Members               │ [19] Update Server Banner │
│ [ 9] Nuke Server                      │ [20] Add Custom Emojis   │
│ [10] Update Server Icon               │ [21] Clear Server        │
│ [11] Delete All Messages              │ [22] Empty Server        │
│ [23] Custom Function 5                │ [24] List All Members    │
│ [25] List All Channels                │ [26] List All Emojis      │
│ [27] Change Server Region             │ [28] Create Categories    │
│ [29] List All Webhooks                │ [30] List All Threads     │
│ [31] Bulk Update Channel Permissions   │ [32] Bulk Update Role Permissions │
└─────────────────────────────────────────────────────────┘
\033[0m
        """)

        try:
            option = int(input("\033[92mSelect an option (1-32): \033[0m"))
            if 1 <= option <= 32:
                await handle_choice(option)
            else:
                print("\033[91mInvalid option. Please select a number between 1 and 32.\033[0m")
        except ValueError:
            print("\033[91mInvalid input. Please enter a number.\033[0m")

async def handle_choice(option):
    guild = bot.get_guild(server_id)
    if guild is None:
        print("\033[91mThe bot is not connected to the server with the specified ID.\033[0m")
        return

    try:
        if option == 1:
            await create_and_delete_channels(guild)
        elif option == 2:
            await rename_server(guild)
        elif option == 3:
            await mass_create_threads(guild)
        elif option == 4:
            await webhook_spammer(guild)
        elif option == 5:
            await delete_webhook(guild)
        elif option == 6:
            await delete_all_webhooks(guild)
        elif option == 7:
            await server_info(guild)
        elif option == 8:
            await rename_all_members(guild)
        elif option == 9:
            await nuke_server(guild)
        elif option == 10:
            await update_server_icon(guild)
        elif option == 11:
            await delete_all_messages(guild)
        elif option == 12:
            await show_all_roles(guild)
        elif option == 13:
            await server_settings(guild)
        elif option == 14:
            await change_channel_description(guild)
        elif option == 15:
            await remove_bots(guild)
        elif option == 16:
            await delete_server(guild)
        elif option == 17:
            await spam_channels(guild)
        elif option == 18:
            await notify_all_members(guild)
        elif option == 19:
            await update_server_banner(guild)
        elif option == 20:
            await add_custom_emojis(guild)
        elif option == 21:
            await clear_server(guild)
        elif option == 22:
            await empty_server(guild)
        elif option == 23:
            await custom_function_5(guild)
        elif option == 24:
            await list_all_members(guild)
        elif option == 25:
            await list_all_channels(guild)
        elif option == 26:
            await list_all_emojis(guild)
        elif option == 27:
            await change_server_region(guild)
        elif option == 28:
            await create_categories(guild)
        elif option == 29:
            await list_all_webhooks(guild)
        elif option == 30:
            await list_all_threads(guild)
        elif option == 31:
            await bulk_update_channel_permissions(guild)
        elif option == 32:
            await bulk_update_role_permissions(guild)
    except Exception as e:
        logging.error(f"Error handling option {option}: {str(e)}")

# Funktion zum Erstellen und Löschen von Kanälen
async def create_and_delete_channels(guild):
    try:
        channel_name = input("Enter base name for channels: ")
        repeat_count = int(input("How many times to repeat create/delete: "))
        for _ in range(repeat_count):
            new_channel = await guild.create_text_channel(f"{channel_name}-{random.randint(1000, 9999)}")
            await new_channel.delete()
        print(f"Repeatedly created and deleted channels {repeat_count} times.")
    except ValueError:
        print("\033[91mInvalid input. Please enter a valid integer.\033[0m")
    except discord.DiscordException as e:
        print(f"\033[91mDiscord API error: {str(e)}\033[0m")
    await menu()

# Funktion zum Umbenennen des Servers
async def rename_server(guild):
    try:
        new_name = input("Enter new server name: ")
        await guild.edit(name=new_name)
        print(f"Server name changed to: {new_name}")
    except discord.Forbidden:
        print("Permission denied to change server name.")
    await menu()

# Funktion zum Massenerstellen von Threads
async def mass_create_threads(guild):
    try:
        channel_id = int(input("Enter channel ID to create threads in: "))
        channel = guild.get_channel(channel_id)
        if channel is None or not isinstance(channel, discord.TextChannel):
            print("\033[91mInvalid channel ID.\033[0m")
            return
        thread_name = input("Enter base name for threads: ")
        thread_count = int(input("How many threads to create: "))
        for _ in range(thread_count):
            await channel.create_thread(name=f"{thread_name}-{random.randint(1000, 9999)}")
        print(f"Created {thread_count} threads.")
    except ValueError:
        print("\033[91mInvalid input. Please enter a valid integer.\033[0m")
    except discord.Forbidden:
        print("\033[91mPermission denied to create threads.\033[0m")
    await menu()

# Funktion zum Webhook-Spamming
async def webhook_spammer(guild):
    try:
        channel_id = int(input("Enter channel ID to spam webhooks in: "))
        channel = guild.get_channel(channel_id)
        if channel is None or not isinstance(channel, discord.TextChannel):
            print("\033[91mInvalid channel ID.\033[0m")
            return
        webhook_name = input("Enter base name for webhooks: ")
        webhook_count = int(input("How many webhooks to spam: "))
        for _ in range(webhook_count):
            await channel.create_webhook(name=f"{webhook_name}-{random.randint(1000, 9999)}")
        print(f"Spammed {webhook_count} webhooks.")
    except ValueError:
        print("\033[91mInvalid input. Please enter a valid integer.\033[0m")
    except discord.Forbidden:
        print("\033[91mPermission denied to create webhooks.\033[0m")
    await menu()

# Funktion zum Löschen eines bestimmten Webhooks
async def delete_webhook(guild):
    try:
        webhook_id = int(input("Enter webhook ID to delete: "))
        webhook = await bot.fetch_webhook(webhook_id)
        await webhook.delete()
        print(f"Deleted webhook with ID: {webhook_id}")
    except ValueError:
        print("\033[91mInvalid webhook ID.\033[0m")
    except discord.NotFound:
        print("\033[91mWebhook not found.\033[0m")
    except discord.Forbidden:
        print("\033[91mPermission denied to delete webhook.\033[0m")
    await menu()

# Funktion zum Löschen aller Webhooks
async def delete_all_webhooks(guild):
    try:
        for channel in guild.text_channels:
            for webhook in await channel.webhooks():
                await webhook.delete()
        print("Deleted all webhooks from all channels.")
    except discord.Forbidden:
        print("\033[91mPermission denied to delete webhooks.\033[0m")
    await menu()

# Funktion zum Anzeigen von Server-Info
async def server_info(guild):
    try:
        info = (
            f"Server Name: {guild.name}\n"
            f"Server ID: {guild.id}\n"
            f"Owner: {guild.owner}\n"
            f"Member Count: {guild.member_count}\n"
            f"Created At: {guild.created_at}\n"
            f"Region: {guild.region}\n"
            f"Verification Level: {guild.verification_level}\n"
            f"Explicit Content Filter: {guild.explicit_content_filter}\n"
        )
        print(info)
    except discord.Forbidden:
        print("\033[91mPermission denied to view server info.\033[0m")
    await menu()

# Funktion zum Umbenennen aller Mitglieder
async def rename_all_members(guild):
    try:
        new_name = input("Enter new name for all members: ")
        for member in guild.members:
            await member.edit(nick=new_name)
        print(f"Renamed all members to: {new_name}")
    except discord.Forbidden:
        print("\033[91mPermission denied to rename members.\033[0m")
    await menu()

# Funktion zum Nuken des Servers
async def nuke_server(guild):
    try:
        # Deletes all channels
        for channel in guild.channels:
            await channel.delete()
        # Create new channels
        for _ in range(10):
            await guild.create_text_channel(f"nuke-channel-{random.randint(1000, 9999)}")
        print("Server has been nuked.")
    except discord.Forbidden:
        print("\033[91mPermission denied to nuke server.\033[0m")
    await menu()

# Funktion zum Aktualisieren des Server-Icons
async def update_server_icon(guild):
    try:
        icon_url = input("Enter URL for new server icon: ")
        async with aiohttp.ClientSession() as session:
            async with session.get(icon_url) as resp:
                if resp.status == 200:
                    image_data = await resp.read()
                    await guild.edit(icon=image_data)
                    print("Server icon updated.")
                else:
                    print("\033[91mFailed to fetch image.\033[0m")
    except discord.Forbidden:
        print("\033[91mPermission denied to update server icon.\033[0m")
    await menu()

# Funktion zum Löschen aller Nachrichten in einem Server
async def delete_all_messages(guild):
    try:
        for channel in guild.text_channels:
            async for message in channel.history(limit=1000):
                await message.delete()
        print("Deleted all messages from all channels.")
    except discord.Forbidden:
        print("\033[91mPermission denied to delete messages.\033[0m")
    await menu()

# Funktion zum Anzeigen aller Rollen
async def show_all_roles(guild):
    try:
        roles = [role.name for role in guild.roles]
        print("Roles in the server:")
        for role in roles:
            print(role)
    except discord.Forbidden:
        print("\033[91mPermission denied to view roles.\033[0m")
    await menu()

# Funktion zum Anzeigen der Server-Einstellungen
async def server_settings(guild):
    try:
        settings = (
            f"Region: {guild.region}\n"
            f"Verification Level: {guild.verification_level}\n"
            f"Explicit Content Filter: {guild.explicit_content_filter}\n"
            f"AFK Channel: {guild.afk_channel}\n"
            f"AFK Timeout: {guild.afk_timeout}\n"
        )
        print("Server settings:")
        print(settings)
    except discord.Forbidden:
        print("\033[91mPermission denied to view server settings.\033[0m")
    await menu()

# Funktion zum Ändern der Kanalbeschreibung
async def change_channel_description(guild):
    try:
        channel_id = int(input("Enter channel ID to update description: "))
        channel = guild.get_channel(channel_id)
        if channel is None or not isinstance(channel, discord.TextChannel):
            print("\033[91mInvalid channel ID.\033[0m")
            return
        new_description = input("Enter new description for the channel: ")
        await channel.edit(topic=new_description)
        print(f"Channel description updated to: {new_description}")
    except ValueError:
        print("\033[91mInvalid channel ID.\033[0m")
    except discord.Forbidden:
        print("\033[91mPermission denied to update channel description.\033[0m")
    await menu()

# Funktion zum Entfernen aller Bots
async def remove_bots(guild):
    try:
        for member in guild.members:
            if member.bot:
                await member.kick(reason="Removing bot")
        print("Removed all bots from the server.")
    except discord.Forbidden:
        print("\033[91mPermission denied to remove bots.\033[0m")
    await menu()

# Funktion zum Löschen des Servers
async def delete_server(guild):
    try:
        await guild.delete()
        print("Server deleted.")
    except discord.Forbidden:
        print("\033[91mPermission denied to delete server.\033[0m")
    await menu()

# Funktion zum Spammen von Kanälen
async def spam_channels(guild):
    try:
        channel_id = int(input("Enter channel ID to spam: "))
        channel = guild.get_channel(channel_id)
        if channel is None or not isinstance(channel, discord.TextChannel):
            print("\033[91mInvalid channel ID.\033[0m")
            return
        message = input("Enter message to spam: ")
        count = int(input("How many messages to send: "))
        for _ in range(count):
            await channel.send(message)
        print(f"Spammed {count} messages in channel {channel_id}.")
    except ValueError:
        print("\033[91mInvalid input. Please enter valid integers.\033[0m")
    except discord.Forbidden:
        print("\033[91mPermission denied to send messages.\033[0m")
    await menu()

# Funktion zum Benachrichtigen aller Mitglieder
async def notify_all_members(guild):
    try:
        for member in guild.members:
            try:
                await member.send("This is a notification.")
            except discord.Forbidden:
                print(f"Could not send message to {member.name}")
        print("Notified all members.")
    except discord.Forbidden:
        print("\033[91mPermission denied to send notifications.\033[0m")
    await menu()

# Funktion zum Aktualisieren des Server-Banners
async def update_server_banner(guild):
    try:
        banner_url = input("Enter URL for new server banner: ")
        async with aiohttp.ClientSession() as session:
            async with session.get(banner_url) as resp:
                if resp.status == 200:
                    image_data = await resp.read()
                    await guild.edit(banner=image_data)
                    print("Server banner updated.")
                else:
                    print("\033[91mFailed to fetch image.\033[0m")
    except discord.Forbidden:
        print("\033[91mPermission denied to update server banner.\033[0m")
    await menu()

# Funktion zum Hinzufügen von benutzerdefinierten Emojis
async def add_custom_emojis(guild):
    try:
        emoji_url = input("Enter URL for new emoji: ")
        emoji_name = input("Enter name for the new emoji: ")
        async with aiohttp.ClientSession() as session:
            async with session.get(emoji_url) as resp:
                if resp.status == 200:
                    image_data = await resp.read()
                    await guild.create_custom_emoji(name=emoji_name, image=image_data)
                    print(f"Added custom emoji: {emoji_name}")
                else:
                    print("\033[91mFailed to fetch image.\033[0m")
    except discord.Forbidden:
        print("\033[91mPermission denied to add custom emojis.\033[0m")
    await menu()

# Funktion zum Leeren des Servers
async def clear_server(guild):
    try:
        for channel in guild.channels:
            await channel.delete()
        await guild.create_text_channel("cleared")
        print("Cleared all channels in the server.")
    except discord.Forbidden:
        print("\033[91mPermission denied to clear server.\033[0m")
    await menu()

# Funktion zum Leeren des Servers
async def empty_server(guild):
    try:
        for member in guild.members:
            if not member.bot:
                await member.kick(reason="Emptying server")
        print("Removed all non-bot members from the server.")
    except discord.Forbidden:
        print("\033[91mPermission denied to empty server.\033[0m")
    await menu()

# Funktion für benutzerdefinierte Funktion 5
async def custom_function_5(guild):
    try:
        print("Custom function 5 is not yet implemented.")
    except discord.Forbidden:
        print("\033[91mPermission denied to perform custom function.\033[0m")
    await menu()

# Funktion zum Auflisten aller Mitglieder
async def list_all_members(guild):
    try:
        members = [member.name for member in guild.members]
        print("Members in the server:")
        for member in members:
            print(member)
    except discord.Forbidden:
        print("\033[91mPermission denied to view members.\033[0m")
    await menu()

# Funktion zum Auflisten aller Kanäle
async def list_all_channels(guild):
    try:
        channels = [channel.name for channel in guild.channels]
        print("Channels in the server:")
        for channel in channels:
            print(channel)
    except discord.Forbidden:
        print("\033[91mPermission denied to view channels.\033[0m")
    await menu()

# Funktion zum Auflisten aller Emojis
async def list_all_emojis(guild):
    try:
        emojis = [emoji.name for emoji in guild.emojis]
        print("Emojis in the server:")
        for emoji in emojis:
            print(emoji)
    except discord.Forbidden:
        print("\033[91mPermission denied to view emojis.\033[0m")
    await menu()

# Funktion zum Ändern der Serverregion
async def change_server_region(guild):
    try:
        new_region = input("Enter new server region: ")
        await guild.edit(region=new_region)
        print(f"Server region updated to: {new_region}")
    except discord.Forbidden:
        print("\033[91mPermission denied to change server region.\033[0m")
    await menu()

# Funktion zum Erstellen von Kategorien
async def create_categories(guild):
    try:
        category_name = input("Enter base name for categories: ")
        for _ in range(5):
            await guild.create_category(f"{category_name}-{random.randint(1000, 9999)}")
        print("Created 5 categories.")
    except discord.Forbidden:
        print("\033[91mPermission denied to create categories.\033[0m")
    await menu()

# Funktion zum Auflisten aller Webhooks
async def list_all_webhooks(guild):
    try:
        for channel in guild.text_channels:
            webhooks = await channel.webhooks()
            for webhook in webhooks:
                print(f"Webhook: {webhook.name} - ID: {webhook.id}")
    except discord.Forbidden:
        print("\033[91mPermission denied to view webhooks.\033[0m")
    await menu()

# Funktion zum Auflisten aller Threads
async def list_all_threads(guild):
    try:
        for channel in guild.text_channels:
            threads = await channel.threads()
            for thread in threads:
                print(f"Thread: {thread.name} - ID: {thread.id}")
    except discord.Forbidden:
        print("\033[91mPermission denied to view threads.\033[0m")
    await menu()

# Funktion zum Mass-Update von Kanalberechtigungen
async def bulk_update_channel_permissions(guild):
    try:
        permission_name = input("Enter the permission to update: ")
        new_value = input("Enter new value for the permission: ")
        for channel in guild.channels:
            await channel.edit(**{permission_name: new_value})
        print(f"Updated {permission_name} for all channels.")
    except discord.Forbidden:
        print("\033[91mPermission denied to update channel permissions.\033[0m")
    await menu()

# Funktion zum Mass-Update von Rollenberechtigungen
async def bulk_update_role_permissions(guild):
    try:
        role_name = input("Enter role name to update permissions: ")
        new_permissions = input("Enter new permissions (comma-separated): ").split(',')
        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            await role.edit(permissions=new_permissions)
            print(f"Updated permissions for role: {role_name}")
        else:
            print("\033[91mRole not found.\033[0m")
    except discord.Forbidden:
        print("\033[91mPermission denied to update role permissions.\033[0m")
    await menu()

# Event-Handler für den Bot-Start
@bot.event
async def on_ready():
    print_title()
    await menu()

# Bot-Token und Server-ID abrufen
bot_token, server_id = get_bot_token_and_server_id()

# Bot starten
bot.run(bot_token)
