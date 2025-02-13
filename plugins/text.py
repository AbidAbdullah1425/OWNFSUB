from pyrogram import Client, filters
import os
from bot import Bot
from config import OWNER_ID

VAR = int(os.environ.get('VAR', 10))  # Load VAR from environment

@Bot.on_message(filters.command("var") & filters.user(OWNER_ID))
async def update_var(client, message):
    global VAR
    try:
        new_value = int(message.text.split()[1])
        os.environ['VAR'] = str(new_value)  # Update the environment variable
        VAR = new_value  # Update the in-memory variable
        await message.reply_text(f"VAR updated to {VAR}")
    except (IndexError, ValueError):
        await message.reply_text("Usage: /var <number>")

@Bot.on_message(filters.command("getvar") & filters.user(OWNER_ID))
async def get_var(client, message):
    await message.reply_text(f"VAR: {VAR}")

