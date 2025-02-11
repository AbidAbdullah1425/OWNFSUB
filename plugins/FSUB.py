import os
from pyrogram import Client, filters
from bot import Bot
from fsub import update_fsub, get_fsub

FILE_PATH = "fsub.txt"

def get_fsub():
    """Retrieve FSUB_1 from file."""
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            return file.read().strip()
    return ""

def update_fsub(channel_id):
    """Update FSUB_1 value in file."""
    with open(FILE_PATH, "w") as file:
        file.write(channel_id)
    return True

@Bot.on_message(filters.command("FSUB_1"))
async def save_fsub(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/FSUB_1 <channel_id>`")
    
    channel_id = message.command[1]
    update_fsub(channel_id)

    await message.reply(f"✅ FSUB_1 updated to `{channel_id}`")

