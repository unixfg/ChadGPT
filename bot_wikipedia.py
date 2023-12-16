import asyncio
import wikipedia
import warnings
from bs4 import GuessedAtParserWarning
from bot_discord import app_commands, discord
from bot_utils import trim_message

# Suppress BeautifulSoup warnings from the Wikipedia library
warnings.filterwarnings("ignore", category=GuessedAtParserWarning)

async def search_wikipedia(query):
    """
    Search Wikipedia for a query and return the URL of the best-matching article.

    Args:
    query (str): The search query.

    Returns:
    str: The URL of the Wikipedia article.
    """
    try:
        loop = asyncio.get_event_loop()

        # Search Wikipedia for the query and get the first result
        search_results = await loop.run_in_executor(None, lambda: wikipedia.search(query))
        if not search_results:
            return f"No results found for '{query}'."

        # Get the page for the first search result
        page_title = search_results[0]
        page = await loop.run_in_executor(None, lambda: wikipedia.page(page_title))
        return page.url

    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]  # Limit to the first 5 options
        options_str = ", ".join(options)
        return f"DisambiguationError: The query '{query}' may refer to: {options_str}. Please be more specific."
    except wikipedia.exceptions.PageError as e:
        return f"PageError: No Wikipedia page found for '{query}'."
    except wikipedia.exceptions.WikipediaException as e:
        return f"WikipediaException: {e}"
    except Exception as e:
        return f"Exception: {e}"

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