import asyncio
import logging
from openai import AsyncOpenAI
from bot_config import load_config, set_logging

config = load_config()
set_logging(config)  # Set up logging configuration
logging.info("Configuration loaded and logging set up.")

def get_behavior(behavior_name):
    behaviors = config['behaviors']
    behavior = next((b for b in behaviors if b['name'] == behavior_name), None)
    if behavior:
        logging.debug(f"Behavior '{behavior_name}' found.")
    else:
        logging.warning(f"Behavior '{behavior_name}' not found.")
    return behavior

# OpenAI API Chat Completion with Behavior
async def ask_openai(prompt, behavior_name):
    openai_client = AsyncOpenAI(api_key=config['openai']['api_key'])

    behavior = get_behavior(behavior_name)
    if not behavior:
        raise ValueError(f"Behavior '{behavior_name}' not found")

    full_prompt = f"{behavior['instructions']} {prompt}"
    logging.debug(f"Sending prompt to OpenAI: {full_prompt}")

    try:
        chat_completion = await openai_client.chat.completions.create(
            messages=[{"role": "user", "content": full_prompt}],
            model=behavior['model'],
        )
        logging.info(f"Received response from OpenAI for behavior '{behavior_name}'.")
        return chat_completion.choices[0].message.content
    except Exception as e:
        logging.error(f"OpenAI API error with behavior '{behavior_name}': {e}")
        return None

# For testing
async def main():
    logging.info("Starting main function.")
    prompt = "Print exactly this: 'OpenAI API is up and responsive.'"
    behavior_name = "Fast"
    response = await ask_openai(prompt, behavior_name)
    if response:
        logging.info(f"OpenAI response: {response}")
    else:
        logging.error("No response received from OpenAI.")
    print(response)

if __name__ == '__main__':
    asyncio.run(main())
