import requests
import yaml

# Load configuration from YAML file
def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def register_command(config_path='config.yaml'):
    config = load_config(config_path)

    TOKEN = config['bot']['token']
    CLIENT_ID = config['bot']['client_id']
    GUILD_ID = config['bot']['guild_id']  # Optional: for registering to a specific guild

    url = f"https://discord.com/api/v8/applications/{CLIENT_ID}/guilds/{GUILD_ID}/commands"  # Guild-specific
    headers = {"Authorization": f"Bot {TOKEN}"}

    # Check if the command already exists
    response = requests.get(url, headers=headers)
    if any(cmd['name'] == 'wiki' for cmd in response.json()):
        print("Command 'wiki' already exists")
    else:
        # Define your command
        json = {
            "name": "wiki",
            "description": "Query information from Wikipedia",
            "options": [
                {
                    "name": "query",
                    "description": "The query to search for",
                    "type": 3,  # Type 3 is 'string'
                    "required": True,
                }
            ]
        }

        response = requests.post(url, headers=headers, json=json)
        print("Status Code", response.status_code)
        print("JSON Response", response.json())

# This makes the script run the function only if it's executed directly, not when imported
if __name__ == '__main__':
    register_command()
