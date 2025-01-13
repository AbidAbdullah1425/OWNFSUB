import logging
from logging.handlers import RotatingFileHandler
from bot import Bot
from config import OWNER_ID, update_fsub_values, collection, LOGGER
from pyrogram import Client, filters


@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command("update"))
async def update_fsubs(client, message):
    update_fsub_values()
    await message.reply("Updated Succesfully")


#update fsub_1 value using commands
def update_fsub1_value()
    new_fsub_value = input("Send new FSUB_1 Channel id")
    if not new_fsub_value.startswith("-100"):
    	print("Invaild fsub1 channel must starts with -100")
    	return
    	
    result = collection.update_one(
    {"_id": "6784b63b7966c6407562bb40"}
    {"$set": {"FSUB_1": new_fsub_value}}
    )
    
    if result.matched_count > 0:
    	print("FSUB_1 updated")
    else:
    	print("Document not found or update unsuccesfull")

@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command("set_fsub1"))
async def setfsub1(client, message)
    if len(message.command) > 2:
        await LOGGER.error("format problem example: /set_fsub1 -100828292922")
        return

    new_fsub_value = message.command[1]
    response = update_fsub1_value(new_fsub_value)
    await message.reply(response)
    