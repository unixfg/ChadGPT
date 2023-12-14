import asyncio
import signal
import logging
import bot_discord
from bot_config import load_config
from bot_database import init_db
from bot_openai import ask_openai

config=load_config()
logging.basicConfig(level=config['logging'].get('level', 'INFO'),format=config['logging']['format'])

db_conn = init_db()

openai_api_online = False

bot = bot_discord.setup_bot()

bot_discord.setup_commands(bot)


@bot.event
async def on_ready():
    global openai_api_online
    test_prompt = "Hello, World!"
    try:
        response = await ask_openai(test_prompt, "Competent")
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
