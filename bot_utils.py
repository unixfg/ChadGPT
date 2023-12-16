# bot_utils.py
from bot_config import load_config

config = load_config()

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
