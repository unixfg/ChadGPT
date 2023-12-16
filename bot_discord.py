import aiohttp
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

# Read the config
from bot_config import load_config
config = load_config()

async def init_bot(TOKEN, CLIENT_ID):
    # Setting intents
    intents = discord.Intents.default()
    intents.guilds = config['bot']['intents'].get('guilds', intents.guilds)
    intents.guild_messages = config['bot']['intents'].get('guild_messages', intents.guild_messages)
    intents.dm_messages = config['bot']['intents'].get('dm_messages', intents.dm_messages)
    intents.message_content = config['bot']['intents'].get('message_content', intents.message_content)

    # Create the bot instance
    bot = commands.Bot(command_prefix=config['bot'].get('command_prefix', "/"), intents=intents)
    return bot

# Test Discord connection
async def test_discord_connection(TOKEN, CLIENT_ID):
    """
    Tests the connection to the Discord API asynchronously.
    """
    url = f"https://discord.com/api/v8/applications/{CLIENT_ID}"
    headers = {"Authorization": f"Bot {TOKEN}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return response.status
        
# For testing
async def main():
    # Test Discord connection
    status = await test_discord_connection(config['bot']['token'], config['bot']['client_id'])
    if status == 200:
        print("Discord API is up and responsive.")
    else:
        print("Discord API is unreachable. Operating in limited mode.")

if __name__ == '__main__':
    asyncio.run(main())
