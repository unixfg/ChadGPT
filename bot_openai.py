from openai import AsyncOpenAI

# Function to find a behavior by name
def get_behavior(behavior_name):
    # Load config
    from bot_config import load_config
    config=load_config()
    behaviors = config['behaviors']
    return next((b for b in behaviors if b['name'] == behavior_name), None)

# OpenAI API Chat Completion with Behavior
async def ask_openai(prompt, behavior_name):
    # Load config
    from bot_config import load_config
    config=load_config()

    # Set up logging
    import logging
    logging.basicConfig(level=config['logging'].get('level', 'INFO'),format=config['logging']['format'])

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
        logging.error(f"OpenAI API error: {e}")
        return None

# For standalone execution
async def main():
    response = await ask_openai("What's your latest corpus update? Print this out as a ready message that confirms you're reachable.", "Competent")
    print(response)

# Execute only if run as a script
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
