import argparse
import asyncio
import signal
import logging
import discord
from bot_utils import setup_license_command
from bot_discord import init_bot, test_discord_connection
from bot_wikipedia import setup_wiki_command
from bot_openai import ask_openai
from bot_database import init_db
from bot_config import load_config, set_logging

config = load_config()
set_logging(config)  # Set up logging configuration
logging.info("Configuration loaded and logging set up.")

# Initialize the database connection
db_path = config['database'].get('path', "db.sqlite3")
db_conn = init_db(db_path)

# Initialize the bot
bot = asyncio.run(init_bot(config['bot']['token'], config['bot']['client_id']))

# Initialize the commands
# Later this should be handled by a plugin system
setup_wiki_command(bot)
setup_license_command(bot)

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

@bot.event
async def on_message(message):
    # Check if the message is a DM
    is_dm = message.channel.type == discord.ChannelType.private
    if is_dm:
        logging.info("Ignoring message in DM.")
        return

    # Check if the bot is mentioned in the message
    if bot.user.mentioned_in(message) and message.author != bot.user:
        logging.info(f"Bot mentioned by {message.author} with message: {message.content}")

        # Extract the message text after the mention
        mention = f'<@!{bot.user.id}>'
        prompt = message.content.replace(mention, '').strip()

        # Call ask_openai function
        try:
            openai_response = await ask_openai(prompt, "Fast")  # Replace "Fast" with your actual behavior name
            if openai_response:
                await message.channel.send(openai_response)
            else:
                await message.channel.send("I couldn't get a response from OpenAI.")
        except Exception as e:
            logging.error(f"Error in OpenAI response: {e}")
            await message.channel.send("An error occurred while processing your request.")

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
