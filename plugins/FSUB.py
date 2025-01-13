import logging
from logging.handlers import RotatingFileHandler
from bot import Bot
from config import OWNER_ID, update_fsub_values, collection, LOGGER
from pyrogram import Client, filters


@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command("update"))
async def update_fsubs(client, message):
    update_fsub_values()
    await message.reply("Updated Successfully")


# Update fsub_1 value using commands
def update_fsub1_value(new_fsub_value):
    if not new_fsub_value.startswith("-100"):
        return "Invalid fsub1 channel, it must start with -100"

    result = collection.update_one(
        {"_id": "6784b63b7966c6407562bb40"},
        {"$set": {"FSUB_1": new_fsub_value}}
    )

    if result.matched_count > 0:
        return "FSUB_1 updated"
    else:
        return "Document not found or update unsuccessful"

@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command("set_fsub1"))
async def setfsub1(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide a valid FSUB_1 channel ID, example: /set_fsub1 -100828292922")
        return

    new_fsub_value = message.command[1]
    response = update_fsub1_value(new_fsub_value)
    await message.reply(response)
