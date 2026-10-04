# Vindictus Guild Chat Filter Bot

Deletes the noisy Discord bridge notice:

> Sent a message to guild chat but has not yet linked their Discord account.

The bot only acts in one configured channel.

## Discord setup

1. Go to the Discord Developer Portal and create a new Application.
2. Open **Bot** and create/add the bot user.
3. Under **Privileged Gateway Intents**, enable **Message Content Intent**.
4. Copy the bot token and place it in a local `.env` file based on `.env.example`.
5. Invite the bot to your server with these channel permissions:
   - View Channel
   - Read Message History
   - Manage Messages
6. In Discord, enable Developer Mode under User Settings > Advanced.
7. Right-click the guild-chat bridge channel, choose **Copy Channel ID**, and place it in `.env` as `TARGET_CHANNEL_ID`.

## Run locally

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
python bot.py
```

## .env example

```env
DISCORD_TOKEN=your_bot_token
TARGET_CHANNEL_ID=123456789012345678
FILTER_TEXT=Sent a message to guild chat but has not yet linked their Discord account.
```

## Notes

- The bot deletes the notice as soon as Discord delivers it, so it may briefly flash for a fraction of a second.
- It does not delete ordinary guild chat messages.
- It also works when the unwanted message was posted by another bot or webhook, provided this bot has **Manage Messages** permission in the channel.
