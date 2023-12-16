import aiohttp
import asyncio
import discord
from discord.ext import commands
import logging
from bot_config import load_config, set_logging

config = load_config()
set_logging(config)  # Set up logging configuration
logging.info("Configuration loaded and logging set up.")

async def init_bot(TOKEN, CLIENT_ID):
    # Setting intents and adding logging
    intents = discord.Intents.default()
    intents.guilds = config['bot']['intents'].get('guilds', intents.guilds)
    intents.guild_messages = config['bot']['intents'].get('guild_messages', intents.guild_messages)
    intents.dm_messages = config['bot']['intents'].get('dm_messages', intents.dm_messages)
    intents.message_content = config['bot']['intents'].get('message_content', intents.message_content)

    # Create the bot instance and log the event
    bot = commands.Bot(command_prefix=config['bot'].get('command_prefix', "/"), intents=intents)
    logging.info("Bot instance created with specified intents.")
    return bot

async def test_discord_connection(TOKEN, CLIENT_ID):
    # Testing Discord connection with logging
    url = f"https://discord.com/api/v8/applications/{CLIENT_ID}"
    headers = {"Authorization": f"Bot {TOKEN}"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            logging.debug(f"Discord API response status: {response.status}")
            return response.status

async def main():
    # Main function with logging
    status = await test_discord_connection(config['bot']['token'], config['bot']['client_id'])
    if status == 200:
        logging.info("Discord API is up and responsive.")
    else:
        logging.warning("Discord API is unreachable. Operating in limited mode.")

if __name__ == '__main__':
    asyncio.run(main())
