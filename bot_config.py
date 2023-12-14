import yaml

def load_config(config_path='config.yaml'):
    """
    Load configuration from a YAML file.

    Args:
    config_path (str): The path to the configuration file.

    Returns:
    dict: The configuration data.
    """
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise Exception(f"Error loading config file: {e}")

# If you want to validate or test loading the config when this file is run directly
if __name__ == '__main__':
    try:
        config = load_config()
        print("Configuration loaded successfully:", config)
    except Exception as error:
        print("Failed to load configuration:", error)