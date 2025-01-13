from bot import Bot
from config import OWNER_ID, update_fsub_values
from pyrogram import Client, filters


@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command('update'))
async def update_fsubs(client, message):
    update_fsub_values()
    await message.reply("Updated Succesfully")
