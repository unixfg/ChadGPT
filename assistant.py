import asyncio
import logging
import sqlite3
import yaml
import signal
import discord
from discord.ext import commands
import openai

# Load configuration from YAML file
def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

config = load_config('config.yaml')

# Configure logging
logging.basicConfig(level=config['logging']['level'], format=config['logging']['format'])

# Initialize the Discord bot
intents = discord.Intents.default()
intents.guilds = config['bot']['intents']['guilds']
intents.guild_messages = config['bot']['intents']['guild_messages']
intents.dm_messages = config['bot']['intents']['dm_messages']
intents.message_content = config['bot']['intents']['message_content']

bot = commands.Bot(command_prefix=config['bot']['command_prefix'], intents=intents)

# Database setup
def init_db():
    conn = sqlite3.connect(config['database']['path'])
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS thread_mapping (
            thread_id TEXT PRIMARY KEY,
            channel_id TEXT
        )
    """)
    # Add more table creation statements as needed
    conn.commit()
    return conn

# Initialize the database
db_conn = init_db()

# Initialize OpenAI client
openai.api_key = config['openai']['api_key']

# OpenAI API Completion
async def ask_openai(prompt):
    try:
        response = openai.Completion.create(
            engine=config['openai']['default_model'],
            prompt=prompt,
            max_tokens=100  # Adjust as needed
        )
        return response.choices[0].text.strip()
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
        else:
            openai_api_online = False
            logging.warning("OpenAI API is unreachable. Operating in limited mode.")
    except Exception as e:
        openai_api_online = False
        logging.error(f"Error in testing OpenAI API: {e}")

    logging.info(f'{bot.user} has connected to Discord and is ready.')

if __name__ == '__main__':
    bot.run(config['bot']['token'])