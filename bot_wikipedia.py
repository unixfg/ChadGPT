import asyncio
import aiohttp
import logging
from bot_discord import app_commands, discord
from bot_utils import trim_message
from bot_config import load_config, set_logging

config = load_config()
set_logging(config)  # Set up logging configuration
logging.info("Configuration loaded and logging set up.")

async def search_wikipedia(query):
    """
    Search Wikipedia using the MediaWiki API and return the URL of the first search result.
    """
    logging.info(f"Starting Wikipedia search for query: {query}")
    URL = "https://en.wikipedia.org/w/api.php"
    PARAMS = {
        "action": "opensearch",
        "namespace": "0",
        "search": query,
        "limit": "1",
        "format": "json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params=PARAMS) as response:
            logging.debug("Wikipedia API request made.")
            data = await response.json()

    if data[1]:
        logging.info(f"Found Wikipedia result for query '{query}': {data[3][0]}")
        return data[3][0]  # URL of the first search result
    else:
        logging.warning(f"No results found for '{query}'.")
        return f"No results found for '{query}'."

def setup_wiki_command(bot):
    @bot.tree.command(name="wiki", description="Query information from Wikipedia")
    @app_commands.describe(query="The query to search for")
    async def wiki(interaction: discord.Interaction, query: str):
        logging.debug(f"Discord bot wiki command triggered with query: {query}")
        await interaction.response.defer()
        response = await search_wikipedia(query)
        trimmed_response = trim_message(response)
        await interaction.followup.send(trimmed_response)
        logging.debug("Wikipedia search result sent to Discord interaction.")

# For testing
async def main():
    logging.info("Starting main function for Wikipedia API test.")
    query = "Hello, World!"
    response = await search_wikipedia(query)
    if response.startswith("https://en.wikipedia.org/wiki/"):
        print("Wikipedia API is up and responsive.")
    else:
        print("Wikipedia API is not responding as expected.")

if __name__ == '__main__':
    asyncio.run(main())
