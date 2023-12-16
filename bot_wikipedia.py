import asyncio
import wikipedia
import warnings
from bs4 import GuessedAtParserWarning
from bot_discord import app_commands, discord
from bot_utils import trim_message

# Suppress BeautifulSoup warnings from the Wikipedia library
warnings.filterwarnings("ignore", category=GuessedAtParserWarning)

def get_wikipedia_page(query):
    """
    Wrapper function to get a Wikipedia page.
    This function will be used with asyncio's run_in_executor.
    """
    return wikipedia.page(query, redirect=True, auto_suggest=True)

async def search_wikipedia(query):
    """
    Search Wikipedia for a query and return the URL of the article.
    """
    try:
        loop = asyncio.get_event_loop()
        page = await loop.run_in_executor(None, get_wikipedia_page, query)
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
    query = "NZT"
    response = await search_wikipedia(query)
    print(response)

if __name__ == '__main__':
    asyncio.run(main())