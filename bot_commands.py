from discord.ext import commands

from bot_main import ask_openai

async def setup_commands(bot):
    @bot.command(name='wiki')
    async def wiki_command(ctx, *, query: str):
        """
        Query AI for Wikipedia article URL.
        """
        prompt = f"Find a Wikipedia URL for: {query}"
        response = await ask_openai(prompt)

        # Process the response to extract URL or provide an appropriate answer
        # For example, checking if response contains a valid URL or information
        if "wikipedia.org" in response:
            logging.info(f"Found Wikipedia URL")
            logging.debug(f"OpenAI API response: {response}")
            await ctx.send(f"{response}")
        else:
            logging.info(f"Did not find Wikipedia URL")
            logging.debug(f"OpenAI API response: {response}")
            await ctx.send(f"{response}")