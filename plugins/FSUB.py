import logging
from bot import Bot
from config import OWNER_ID, redis_client, LOGGER, FSUB_1, FSUB_2, FSUB_3, FSUB_4
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Helper to fetch FSUB value with fallback to default
def get_fsub_value(fsub_key, default_value):
    return redis_client.get(fsub_key) or default_value

# Command: /set_fsub [fsub_key] [new_value]
@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command("set_fsub"))
async def set_fsub(client, message):
    command_parts = message.text.split(" ", 2)
    
    if len(command_parts) < 3:
        LOGGER.warning("Invalid command. Expected format: /set_fsub [fsub_key] [new_value]")
        return

    fsub_key = command_parts[1].strip().upper()  # e.g., FSUB_1
    new_value = command_parts[2].strip()         # e.g., -1001234567890
    
    if fsub_key not in ["FSUB_1", "FSUB_2", "FSUB_3", "FSUB_4"]:
        LOGGER.warning(f"Invalid FSUB key: {fsub_key}. Allowed keys: FSUB_1, FSUB_2, FSUB_3, FSUB_4")
        return

    if not new_value.startswith("-100"):
        LOGGER.warning(f"Invalid {fsub_key} value, it must start with -100")
        return

    # Update FSUB value in Redis
    redis_client.set(fsub_key, new_value)
    LOGGER.info(f"{fsub_key} updated successfully to {new_value}")
    await message.reply(f"{fsub_key} updated successfully to {new_value}")

# Command: /show_fsubs
@Bot.on_message(filters.private & filters.user(OWNER_ID) & filters.command("show_fsubs"))
async def show_fsubs(client, message):
    # Fetch current FSUB values with fallback to config defaults
    fsub_values = {
        "FSUB_1": get_fsub_value("FSUB_1", FSUB_1),
        "FSUB_2": get_fsub_value("FSUB_2", FSUB_2),
        "FSUB_3": get_fsub_value("FSUB_3", FSUB_3),
        "FSUB_4": get_fsub_value("FSUB_4", FSUB_4),
    }

    # Generate buttons for editing FSUB values
    buttons = []
    for key, value in fsub_values.items():
        buttons.append([InlineKeyboardButton(f"Edit {key}", callback_data=f"edit_{key}")])

    # Construct response
    response = "Current FSUB Variables:\n\n"
    response += "\n".join([f"{key}: {value}" for key, value in fsub_values.items()])

    await message.reply(
        response,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Callback handler for editing FSUB values
@Bot.on_callback_query(filters.regex(r"^edit_(FSUB_\d)$"))
async def edit_fsub_callback(client, callback_query):
    fsub_key = callback_query.data.split("_")[1]
    await callback_query.message.reply(
        f"Send the new value for {fsub_key}. Example: -1001234567890",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Cancel", callback_data="cancel_edit")]]
        )
    )
    # Store the key being edited in Redis for the user session
    redis_client.set(f"editing_{callback_query.from_user.id}", fsub_key)

# Command handler for providing the new FSUB value
@Bot.on_message(filters.private & filters.user(OWNER_ID))
async def set_fsub_from_callback(client, message):
    editing_key = redis_client.get(f"editing_{message.from_user.id}")
    if not editing_key:
        return  # No active editing session
    
    new_value = message.text.strip()
    if not new_value.startswith("-100"):
        await message.reply("Invalid value. Channel ID must start with -100.")
        return

    # Update the FSUB value and clear the editing session
    redis_client.set(editing_key, new_value)
    redis_client.delete(f"editing_{message.from_user.id}")
    await message.reply(f"{editing_key} updated successfully to {new_value}")
    LOGGER.info(f"{editing_key} updated successfully to {new_value}")

# Cancel editing
@Bot.on_callback_query(filters.regex(r"^cancel_edit$"))
async def cancel_edit_callback(client, callback_query):
    redis_client.delete(f"editing_{callback_query.from_user.id}")
    await callback_query.message.reply("Edit operation cancelled.")
