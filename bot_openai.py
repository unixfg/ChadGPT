import asyncio
import logging
from bot_openai import AsyncOpenAI
from bot_config import load_config

# Load configuration from YAML file
config = load_config('config.yaml')
openai_client = AsyncOpenAI(api_key=config['openai']['api_key'])

# Define the behaviors
behaviors = config['behaviors']

# Function to find a behavior by name
def get_behavior(behavior_name):
    return next((b for b in behaviors if b['name'] == behavior_name), None)

# OpenAI API Chat Completion with Behavior
async def ask_openai(prompt, behavior_name):
    behavior = get_behavior(behavior_name)
    if not behavior:
        raise ValueError(f"Behavior '{behavior_name}' not found")

    full_prompt = f"{behavior['instructions']} {prompt}"
    try:
        chat_completion = await openai_client.chat.completions.create(
            messages=[{"role": "user", "content": full_prompt}],
            model=behavior['model'],
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return None

# For standalone execution
async def main():
    response = await ask_openai("What's the weather like today?", "Competent")
    print(response)

# Execute only if run as a script
if __name__ == '__main__':
    asyncio.run(main())
