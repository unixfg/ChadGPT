import asyncio
import wikipedia

async def search_wikipedia(query):
    """
    Search Wikipedia for a query and return the URL of the article.

    Args:
    query (str): The search query.

    Returns:
    str: The URL of the Wikipedia article.
    """
    try:
        loop = asyncio.get_event_loop()
        page = await loop.run_in_executor(None, wikipedia.page, query)
        return page.url
    except wikipedia.exceptions.DisambiguationError as e:
        return f"DisambiguationError: {e}"
    except wikipedia.exceptions.PageError as e:
        return f"PageError: {e}"
    except wikipedia.exceptions.WikipediaException as e:
        return f"WikipediaException: {e}"
    except Exception as e:
        return f"Exception: {e}"
