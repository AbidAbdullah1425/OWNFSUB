from pyrogram import Client, filters
from bot import Bot
from config import OWNER_ID, VAR  # Import the VAR from config
import libimport

@Bot.on_message(filters.command("var") & filters.user(OWNER_ID))
async def update_var(client, message):
    global VAR  # Ensure we're using the global VAR variable
    try:
        new_value = int(message.text.split()[1])
        # Modify the variable
        VAR = new_value
        
        # Dynamically reload the config.py module to apply changes
        libimport.reload('config')
        
        await message.reply_text(f"VAR updated to {VAR}")
    except (IndexError, ValueError):
        await message.reply_text("Usage: /var <number>")

@Bot.on_message(filters.command("getvar") & filters.user(OWNER_ID))
async def get_var(client, message):
    # Always fetch the latest value after reloading
    latest_var = VAR  # VAR will be updated after reload
    await message.reply_text(f"VAR: {latest_var}")

