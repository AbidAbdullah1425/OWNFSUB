import os, sys
from bot import Bot
from config import OWNER_ID, FSUB_1
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid


@Bot.on_message(filters.private & filters.command("restart") & filters.user(OWNER_ID))
async def restart_bot(b, m):
    global is_restarting
    if not is_restarting:
        is_restarting = True
        await m.reply_text("**🔄 Restarting.....**")

        # Gracefully stop the bot's event loop
        b.stop()
        time.sleep(2)  # Adjust the delay duration based on your bot's shutdown time

        # Restart the bot process
        os.execl(sys.executable, sys.executable, *sys.argv)

    
