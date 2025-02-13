from pyrogram import Client, filters
import os
from bot import Bot
from config import OWNER_ID

VAR = int(os.environ.get('VAR', 10))  # Load VAR from environment

@Bot.on_message(filters.command("var") & filters.user(OWNER_ID))
async def update_var(client, message):
    try:
        new_value = int(message.text.split()[1])
        os.environ['VAR'] = str(new_value)  # Update the environment variable
        await message.reply_text(f"VAR updated to {new_value}")
    except (IndexError, ValueError):
        await message.reply_text("Usage: /var <number>")

@Bot.on_message(filters.command("getvar") & filters.user(OWNER_ID))
async def get_var(client, message):
    latest_var = int(os.environ.get('VAR', 10))  # Always fetch the latest value
    await message.reply_text(f"VAR: {latest_var}")

