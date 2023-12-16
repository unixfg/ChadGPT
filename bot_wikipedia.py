import asyncio
import aiohttp
from bot_discord import app_commands, discord
from bot_utils import trim_message

async def search_wikipedia(query):
    """
    Search Wikipedia using the MediaWiki API and return the URL of the first search result.

    Args:
    query (str): The search query.

    Returns:
    str: The URL of the Wikipedia article.
    """
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
            data = await response.json()

    if data[1]:
        return data[3][0]  # URL of the first search result
    else:
        return f"No results found for '{query}'."

def setup_wiki_command(bot):
    @bot.tree.command(name="wiki", description="Query information from Wikipedia")
    @app_commands.describe(query="The query to search for")
    async def wiki(interaction: discord.Interaction, query: str):
        await interaction.response.defer()
        response = await search_wikipedia(query)
        trimmed_response = trim_message(response)
        await interaction.followup.send(trimmed_response)

# For testing
async def main():
    query = "Hello, World!"
    response = await search_wikipedia(query)
    print(response)

if __name__ == '__main__':
    asyncio.run(main())