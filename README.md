# ChadGPT Bot

ChadGPT is a Discord bot with a unique twist, combining cutting-edge AI with a personality that's confident, humorous, and user-centric. It's designed to engage users in a playful yet privacy-respecting manner.

## Design Philosophy

- **Unique "ChadGPT" Theme**: Maintains a distinctive personality and style that sets it apart.
- **Privacy First Approach**: Emphasizes user privacy with an opt-in system, except in a designated bot channel.

### Fixed User Tiers

#### a. Admin
#### b. Plus
#### c. Standard

### Commands
- **/help**: Displays a list of commands and their descriptions.
- **/about**: Displays information about the bot experience. Example usage: `/about`
- **/optin**: Opt-in to the bot. This is required to use the bot outside of the bot channel. Example usage: `/optin`
- **/optout**: Opt-out of the bot. This is required to stop using the bot outside of the bot channel. Example usage: `/optout`
- **/forget**: Forget the user. This is required to remove user data from the bot. Example usage: `/forget [me, user, channel] <user, channel>`
- **/set**: Set a preference. Example usage: 
    - `/set system <preference> <value>` (Admin only)
    - `/set channel [channel_id] <preference> <value>` (Admin only, defaulting to current channel if not present)
    - `/set user <user_name> <preference> <value>` (Self only, unless Admin)
- **/get**: Get a preference. Example usage:
    - `/get system <preference>` (Admin only)
    - `/get channel [channel_id] <preference>` (Admin only, defaulting to current channel if not present)
    - `/get user <user_name> <preference>` (Self only, unless Admin)

## Data Structures
- **thread_id**: A unique identifier for an OpenAI thread.
- **channel_id**: A unique identifier for a Discord channel or DM.
- **user_id**: A unique identifier for a Discord user.
- **user_tier**: A user tier that determines the bot's behavior.
- **user_preferences**: A set of user preferences that determine the bot's behavior.
    - `opt_in`: A boolean indicating whether the user has opted in to use the bot.
    - `model`: The name of the OpenAI model the user prefers. (overrides behavior model)
    - `behavior`: The name of the behavior the user prefers.
- **system_preferences**: A set of system preferences that determine the bot's behavior.
- **channel_preferences**: A set of channel preferences that determine the bot's behavior.
    - `opt_in`: A boolean indicating all channel users have opted in to use the bot.
    - `model`: The name of the OpenAI model the user prefers. (overrides behavior model)
    - `behavior`: The name of the behavior the user prefers.

## Additional Considerations
- **Interactive Channel**: A special channel where all messages prompt the bot for a response. However, ChadGPT decides autonomously whether to engage, based on the content.
- **Command System**: A command system that allows users to interact with the bot and the bot to interact with script functions. Users can execute bot commands with the standard `/` prefix, and the bot can execute script functions by returning the `!` prefix.
- **Dynamic Configuration**: User preferences and overrides of *select* YAML file defaults and behaviors can be set via commands and stored in the database.
- **User Privacy**: No user data is stored without consent, except for the bot channel. User should be able to have the bot "forget" them but that will be hard to implement for channels without impacting everyone.
- **Bot Channel**: The bot channel is a special channel where the bot will always respond to messages. This is the only channel where the bot will respond without user consent. This is also the only channel where the bot will respond to commands without user consent.

---