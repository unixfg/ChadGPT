import sys
import requests
import argparse
import aiohttp
import asyncio
import signal
from bot_openai import ask_openai

# Load config
from bot_config import load_config
config=load_config()

# Set up logging
import logging
logging.basicConfig(level=config['logging'].get('level', 'INFO'),format=config['logging']['format'])

# Initialize the database connection
from bot_database import init_db
db_conn = init_db()

# Initialize the Discord bot with intents
import discord
from discord import app_commands
from discord.ext import commands
intents = discord.Intents.default()

# Setting intents based on the config
intents.guilds = config['bot']['intents'].get('guilds', intents.guilds)
intents.guild_messages = config['bot']['intents'].get('guild_messages', intents.guild_messages)
intents.dm_messages = config['bot']['intents'].get('dm_messages', intents.dm_messages)
intents.message_content = config['bot']['intents'].get('message_content', intents.message_content)

# Create the bot instance
bot = commands.Bot(command_prefix=config['bot'].get('command_prefix', "/"), intents=intents)

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

# Define a slash command
@bot.tree.command(name="wiki", description="Query information from Wikipedia")
@app_commands.describe(query="The query to search for")
async def wiki(interaction: discord.Interaction, query: str):
    await interaction.response.defer()
    """
    Query AI for Wikipedia article URL.
    """
    prompt = f"{query}"
    # Validate that openai_api_online is True
    if not openai_api_online:
        await interaction.response.send_message(config['messages']['offline'])
        return
    response = await ask_openai(prompt, "Wiki")

    if interaction.response.is_done():
        # Follow-up with an additional message
        await interaction.followup.send(f"{response}")
    else:
        # Send initial response
        await interaction.response.send_message(f"{response}")

@bot.event
async def on_ready():
    global openai_api_online
    test_prompt = "Hello, World!"
    try:
        response = await ask_openai(test_prompt, "Fast")
        if response:
            openai_api_online = True
            logging.info("OpenAI API is up and responsive.")
            logging.debug(f"OpenAI API response: {response}")
        else:
            openai_api_online = False
            logging.warning("OpenAI API is unreachable. Operating in limited mode.")
    except Exception as e:
        openai_api_online = False
        logging.error(f"Error in testing OpenAI API: {e}")

    logging.info(f'{bot.user} has connected to Discord and is ready.')

async def shutdown():
    logging.info("Completing shutdown...")

    # Cancel all remaining tasks
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]

    await asyncio.gather(*tasks, return_exceptions=True)

    # Close the bot
    await bot.close()

    # Close the database connection
    if db_conn:
        db_conn.close()

    logging.info("Bot has shut down successfully.")

def signal_handler(signum, frame):
    logging.info("Shutdown initiated, please wait...")
    asyncio.create_task(shutdown())

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Main execution
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ChadGPT Discord Bot')
    parser.add_argument('--test', action='store_true', help='Test the Discord connection')

    args = parser.parse_args()

    if args.test:
        loop = asyncio.get_event_loop()
        print(loop.run_until_complete(test_discord_connection(config['bot']['token'], config['bot']['client_id'])))
        loop.close()
    else:
        # Create a new event loop and set it as the current event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(bot.start(config['bot']['token']))
        except asyncio.CancelledError:
            # Suppress the CancelledError
            pass
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
