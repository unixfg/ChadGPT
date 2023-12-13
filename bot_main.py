import asyncio
import logging
import sqlite3
import yaml
import signal
import discord
from discord.ext import commands
from openai import AsyncOpenAI

# Load configuration from YAML file
def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

config = load_config('config.yaml')

# Configure logging
logging.basicConfig(level=config['logging'].get('level', 'INFO'), format=config['logging']['format'])

# Initialize the Discord bot
intents = discord.Intents.default()
intents.guilds = config['bot']['intents'].get('guilds', True)
intents.guild_messages = config['bot']['intents'].get('guild_messages', True)
intents.dm_messages = config['bot']['intents'].get('dm_messages', True)
intents.message_content = config['bot']['intents'].get('message_content', True)

bot = commands.Bot(command_prefix=config['bot'].get('command_prefix', "/"), intents=intents)

from bot_commands import setup_commands
asyncio.run(setup_commands(bot))

# Database setup
def init_db():
    conn = sqlite3.connect(config['database'].get('path', "db.sqlite3"))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS thread_mapping (
            thread_id TEXT PRIMARY KEY,
            channel_id TEXT
        )
    """)
    conn.commit()
    return conn

db_conn = init_db()

# Initialize OpenAI Async client
openai_client = AsyncOpenAI(api_key=config['openai']['api_key'])

# OpenAI API Chat Completion
async def ask_openai(prompt):
    try:
        chat_completion = await openai_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=config['openai'].get('default_model', "gpt-3.5-turbo"),
        )
        # Accessing the response content
        return chat_completion.choices[0].message.content
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return None

# Global variable to track OpenAI API availability
openai_api_online = False

@bot.event
async def on_ready():
    global openai_api_online
    test_prompt = "Hello, World!"
    try:
        response = await ask_openai(test_prompt)
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

# Graceful shutdown
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
