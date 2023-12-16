import yaml
import asyncio
import os
import logging

def load_config(config_path='config.yaml'):
    """
    Load configuration from a YAML file. Uses the given path, or if a relative path is provided,
    it uses the script's location as the base.

    Args:
    config_path (str): The path to the configuration file.

    Returns:
    dict: The configuration data or None if loading fails.
    """
    # Check if the provided path is absolute
    if not os.path.isabs(config_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, config_path)

    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML file: {e}")
    except Exception as e:
        raise Exception(f"Error loading config file: {e}")

    return None  # or return a default configuration

# For testing
async def main():
    config = load_config()

    if config:
        logging.basicConfig(level=config['logging'].get('level', 'INFO'),
                            format=config['logging']['format'])
    else:
        # Set a default logging configuration if config loading fails
        logging.basicConfig(level=logging.INFO)

    if __name__ == '__main__':
        config_path = os.getenv('CONFIG_PATH', 'config.yaml')
        configuration = load_config(config_path)
        if configuration:
            print("Configuration loaded successfully.")
        else:
            print("Failed to load configuration")

if __name__ == '__main__':
    asyncio.run(main())
