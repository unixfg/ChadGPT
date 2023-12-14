import yaml
import os

def load_config(config_path='config.yaml'):
    """
    Load configuration from a YAML file. Uses the given path, or if a relative path is provided,
    it uses the script's location as the base.

    Args:
    config_path (str): The path to the configuration file. It can be an absolute path or relative to the script's location.

    Returns:
    dict: The configuration data.
    """
    # Check if the provided path is absolute
    if not os.path.isabs(config_path):
        # If not, prepend the script's directory to it
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, config_path)

    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise Exception(f"Error loading config file: {e}")

if __name__ == '__main__':
    try:
        # Example usage: you can pass a full path or just a filename
        configuration = load_config('config.yaml')
        print("Configuration loaded successfully:", configuration)
    except Exception as error:
        print("Failed to load configuration:", error)