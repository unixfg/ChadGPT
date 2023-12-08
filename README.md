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
- **Thread-Channel Mapping**:
  - `thread_id`: A unique identifier for an OpenAI thread.
  - `channel_id`: A unique identifier for a Discord channel or DM.
- **User Data**:
  - `user_id`: A unique identifier for a Discord user.
  - `user_tier`: Classification for the bot's behavior.
  - `user_preferences`: Customizable settings for bot interaction.
    - `opt_in`: Boolean indicating consent to interact with the bot.
    - `model`: Preferred OpenAI model for responses.
    - `behavior`: Preset behavior pattern for bot interaction.
- **System Preferences**:
  - Global settings influencing the bot's behavior.
- **Channel Preferences**:
  - Settings specific to each Discord channel.
    - `opt_in`: Boolean for channel-wide bot interaction consent.
    - `model`: Preferred OpenAI model for the channel.
    - `behavior`: Behavior pattern for the channel.

## Additional Considerations
- **Interactive Channel**: A channel for free-form interaction with autonomous response decisions by ChadGPT.
- **Command System**: Allows interaction with the bot and script function execution.
- **Dynamic Configuration**: Configuration adjustments via commands, influencing behavior and preferences.
- **User Privacy**: Commitment to data privacy and user consent, with options for data removal.
- **Bot Channel**: A dedicated channel for unrestricted bot interaction.
- **Privacy Settings**: Handling of user data, data storage duration, and security measures.
- **Rate Limiting and Usage Quotas**: Management of message/command frequency by user tier.
- **Fallback Mechanisms**: Default responses or model switching in case of AI response generation issues.

---
