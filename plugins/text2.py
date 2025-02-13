import importlib
from plugins.text import VAR  # Import the VAR variable
from bot import Bot
from pyrogram import filters
import config  # Import config to reload it
from config import OWNER_ID

@Bot.on_message(filters.command("checkvar") & filters.user(OWNER_ID))
async def get_var(client, message):
    # Reload the config module to get the latest VAR value
    importlib.reload(config)  # This reloads the config module
    from plugins.text import VAR  # Re-import VAR after reload

    # Send the latest value of VAR
    await message.reply_text(f"VAR: {VAR}")
