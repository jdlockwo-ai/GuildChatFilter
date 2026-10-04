import os
import logging
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID", "0"))
FILTER_TEXT = os.getenv(
    "FILTER_TEXT",
    "Sent a message to guild chat but has not yet linked their Discord account."
).strip().lower()

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set")
if not TARGET_CHANNEL_ID:
    raise RuntimeError("TARGET_CHANNEL_ID is not set")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

intents = discord.Intents.default()
intents.message_content = True

class FilterBot(discord.Client):
    async def on_ready(self):
        logging.info("Logged in as %s (%s)", self.user, self.user.id)
        logging.info("Filtering channel ID: %s", TARGET_CHANNEL_ID)

    async def on_message(self, message: discord.Message):
        # Only act in the configured guild-chat bridge channel.
        if message.channel.id != TARGET_CHANNEL_ID:
            return

        # Ignore this bot's own messages.
        if self.user and message.author.id == self.user.id:
            return

        content = (message.content or "").strip().lower()

        # Delete only the unwanted bridge notice. Using "in" also catches
        # duplicate/combined versions of the same notice.
        if FILTER_TEXT and FILTER_TEXT in content:
            try:
                await message.delete()
                logging.info(
                    "Deleted filtered message from %s (author=%s, webhook_id=%s)",
                    message.channel,
                    message.author,
                    message.webhook_id,
                )
            except discord.Forbidden:
                logging.error("Missing Manage Messages permission in channel %s", message.channel)
            except discord.NotFound:
                pass
            except discord.HTTPException as exc:
                logging.exception("Discord API error while deleting message: %s", exc)

client = FilterBot(intents=intents)
client.run(TOKEN)
