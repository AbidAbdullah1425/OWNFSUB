from text import VAR
from bot import Bot

@Bot.on_message(filters.command("checkvar") & filters.user(OWNER_ID))
async def get_var(client, message):
    await message.reply_text(f"VAR: {VAR}")