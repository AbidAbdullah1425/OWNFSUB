import os
from pyrogram import filters
from pyrogram.types import Message
from config import OWNER_ID, LOGGER
from bot import Bot

@Bot.on_message(filters.command("restart") & filters.user(OWNER_ID))
async def restart_bot(_, message: Message):
    try:
        msg = await message.reply_text("`Restarting bot...`")
        LOGGER(__name__).info("Attempting to restart bot...")
    except Exception as e:
        LOGGER(__name__).exception(f"Error while restarting bot: {e}")
        await msg.edit_text("❌ Failed to initiate restart.")
        return
    
    try:
        # Gracefully stop the bot
        await bot_instance.stop()
    except Exception as e:
        LOGGER(__name__).exception(f"Error while stopping bot: {e}")
        await msg.edit_text("❌ Failed to stop the bot.")
        return
    
    try:
        # Start the bot again (assuming 'bash start' is correct for your setup)
        os.system("bash start &")
    except Exception as e:
        LOGGER(__name__).exception(f"Error while starting bot: {e}")
        await msg.edit_text("❌ Failed to start the bot after stopping.")
        return
    
    await msg.edit_text("✅ Bot has restarted successfully!")
