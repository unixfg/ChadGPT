import logging
import yaml

def setup_logging():
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        logging.basicConfig(level=config['logging'].get('level', 'INFO'),
                            format=config['logging']['format'])

# Call the function immediately to configure logging at import time
setup_logging()