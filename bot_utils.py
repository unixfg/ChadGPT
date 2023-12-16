# bot_utils.py
import logging
from bot_config import load_config, set_logging

config = load_config()
set_logging(config)  # Set up logging configuration
logging.info("Configuration loaded and logging set up.")

def trim_message(message, suffix="..."):
    """
    Trims the message to a maximum length specified in the config or default to 2000.

    Args:
    message (str): The message to be trimmed.
    suffix (str, optional): A suffix to add at the end if the message is trimmed. Defaults to "...".

    Returns:
    str: The trimmed message.
    """
    max_length = config['bot'].get('max_length', 2000)
    if len(message) > max_length:
        return message[:max_length - len(suffix)] + suffix
    return message
