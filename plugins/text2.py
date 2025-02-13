from plugins.text import VAR  # Import from the correct path
from bot import Bot
from pyrogram import filters
from config import OWNER_ID

@Bot.on_message(filters.command("checkvar") & filters.user(OWNER_ID))
async def get_var(client, message):
    await message.reply_text(f"VAR: {VAR}")
