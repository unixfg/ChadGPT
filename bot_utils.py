# bot_utils.py
import logging
import discord
import asyncio
from discord.ext import commands
from bot_config import load_config, set_logging

config = load_config()
set_logging(config)  # Set up logging configuration
logging.info("Configuration loaded and logging set up.")

def trim_message(message, max_length=None, suffix="..."):
    """
    Trims the message to a maximum length specified in the argument or config.

    Args:
    message (str): The message to be trimmed.
    max_length (int, optional): The maximum length for the message. If not specified, defaults to the config value.
    suffix (str, optional): A suffix to add at the end if the message is trimmed. Defaults to "...".
    
    Returns:
    str: The trimmed message.
    """
    # Use the provided max_length or default to the config value
    max_length = max_length or config['bot'].get('max_length', 2000)

    if len(message) > max_length:
        return message[:max_length - len(suffix)] + suffix
    return message

def setup_license_command(bot: commands.Bot):
    @bot.tree.command(name='license', description='Display the bot\'s license information')
    async def license(interaction: discord.Interaction):
        license_url = "https://www.gnu.org/licenses/agpl-3.0.html"
        response = f"This bot is licensed under the AGPL-3.0 License.\nLicense Details: {license_url}"
        await interaction.response.send_message(response)

async def main():
    logging.info("Starting main function for bot_utils test.")
    message = "Hello, World! This is a test message to check the trimming functionality."

    # Test with default max_length from config
    trimmed_message_default = trim_message(message)
    print(f"Default trimmed message: {trimmed_message_default}")

    # Test with custom max_length
    custom_max_length = 15
    trimmed_message_custom = trim_message(message, max_length=custom_max_length)
    print(f"Custom trimmed message ({custom_max_length} chars): {trimmed_message_custom}")

if __name__ == '__main__':
    asyncio.run(main())