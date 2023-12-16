import asyncio
import logging
from openai import AsyncOpenAI
from bot_config import load_config

config = load_config()

def get_behavior(behavior_name):
    behaviors = config['behaviors']
    return next((b for b in behaviors if b['name'] == behavior_name), None)

# OpenAI API Chat Completion with Behavior
async def ask_openai(prompt, behavior_name):
    openai_client = AsyncOpenAI(api_key=config['openai']['api_key'])

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
        logging.error(f"OpenAI API error with behavior '{behavior_name}': {e}")
        return None

async def main():
    # Example usage with command-line arguments
    prompt = "Print a ready message"
    behavior_name = "Fast"
    response = await ask_openai(prompt, behavior_name)
    print(response)

if __name__ == '__main__':
    asyncio.run(main())
    