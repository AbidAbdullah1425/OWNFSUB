import logging
from logging.handlers import RotatingFileHandler
from bot import Bot
from config import OWNER_ID, update_fsub_values, collection, LOGGER, FSUB_1, FSUB_2, FSUB_3, FSUB_4
from pyrogram import Client, filters
from bson import ObjectId  # Import ObjectId


# Refresh FSUB values after an update
@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command("update"))
async def update_fsubs(client, message):
    update_fsub_values()  # Update the values from MongoDB
    await message.reply("Updated Successfully")

# Update fsub_1 value using commands
def update_fsub1_value(new_fsub_value):
    if not new_fsub_value.startswith("-100"):
        # Log the warning correctly without await
        LOGGER.warning("Invalid fsub1 channel, it must start with -100")
        return "Invalid fsub1 channel, it must start with -100"

    # Perform the update operation
    result = collection.update_one(
        {"_id": ObjectId("6784b63b7966c6407562bb40")},  # Use ObjectId here
        {"$set": {"FSUB_1": new_fsub_value}}
    )

    # Check if the document was updated
    if result.matched_count > 0:
        # Refresh FSUB values after the update
        update_fsub_values()

        # Fetch the updated document to confirm the change
        updated_document = collection.find_one({"_id": ObjectId("6784b63b7966c6407562bb40")})
        updated_fsub_value = updated_document.get("FSUB_1")

        if updated_fsub_value == new_fsub_value:
            return f"FSUB_1 updated successfully to {new_fsub_value}"
        else:
            return "Update failed, FSUB_1 value not changed in database"
    else:
        return "Document not found or update unsuccessful"

@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command("set_fsub1"))
async def setfsub1(client, message):
    if len(message.command) < 2:
        LOGGER.warning("Please provide a valid FSUB_1 channel ID, example: /set_fsub1 -100828292922")
        return

    new_fsub_value = message.command[1]
    response = update_fsub1_value(new_fsub_value)

    await message.reply(response)

@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command("channels"))
async def showfsub(client, message):
    response = (
        "Current FSUB Variables:\n\n"
        f"FSUB_1: {FSUB_1}\n"
        f"FSUB_2: {FSUB_2}\n"
        f"FSUB_3: {FSUB_3}\n"
        f"FSUB_4: {FSUB_4}\n"
    )


    await message.reply(response)
