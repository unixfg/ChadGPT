import discord
from discord.ext import commands

def setup_bot():
    # Load config
    from bot_config import load_config
    config=load_config()

    # Set up logging
    import logging
    logging.basicConfig(level=config['logging'].get('level', 'INFO'),format=config['logging']['format'])

    # Initialize the Discord bot with intents
    intents = discord.Intents.default()
    intents.guilds = config['bot']['intents'].get('guilds', True)
    intents.guild_messages = config['bot']['intents'].get('guild_messages', True)
    intents.dm_messages = config['bot']['intents'].get('dm_messages', True)
    intents.message_content = config['bot']['intents'].get('message_content', True)

    # Create the bot instance
    bot = commands.Bot(command_prefix=config['bot'].get('command_prefix', "/"), intents=intents)
    return bot

def setup_commands(bot):
    # Load config
    from bot_config import load_config
    config=load_config()

    # Set up logging
    import logging
    logging.basicConfig(level=config['logging'].get('level', 'INFO'),format=config['logging']['format'])

    @bot.command(name='wiki')
    async def wiki_command(ctx, *, query: str):
        """
        Query AI for Wikipedia article URL.
        """
        from bot_openai import ask_openai  # Import here to avoid circular dependency

        prompt = f"Find a Wikipedia URL for: {query}"
        response = await ask_openai(prompt)

        if "wikipedia.org" in response:
            logging.info("Found Wikipedia URL")
            await ctx.send(response)
        else:
            logging.info("Did not find Wikipedia URL")
            await ctx.send(response)
            