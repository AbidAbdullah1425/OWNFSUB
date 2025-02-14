import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import DB_URI
import pymongo
import importlib
import config
from plugins import invitelinks
from invitelinks import generate_invite_links  # We will call this function for fallback invite links

# MongoDB connection
client = pymongo.MongoClient(DB_URI)
db = client['bot_config']
fsub_collection = db['fsub_channels']

# Reload config and invitelinks
def reload_modules():
    importlib.reload(config)  # Reload config.py
    importlib.reload(invitelinks)  # Reload invitelinks.py

# Get the latest FSUB values from MongoDB
def get_fsub_data():
    fsub_data = fsub_collection.find_one({"_id": "fsub_data"})
    if fsub_data:
        return fsub_data.get("FSUB_1"), fsub_data.get("FSUB_2"), fsub_data.get("FSUB_3"), fsub_data.get("FSUB_4")
    return None, None, None, None

# Save the updated FSUB values to MongoDB
def save_fsub_data(fsub_1, fsub_2, fsub_3, fsub_4):
    fsub_data = {
        "_id": "fsub_data",  # Ensures only one document for FSUB
        "FSUB_1": fsub_1,
        "FSUB_2": fsub_2,
        "FSUB_3": fsub_3,
        "FSUB_4": fsub_4
    }
    fsub_collection.replace_one({"_id": "fsub_data"}, fsub_data, upsert=True)  # Save or update

# Command: /fsub
@Client.on_message(filters.command('fsub') & filters.user(OWNER_ID) & filters.private)
async def fsub(client: Client, message: Message):
    await message.reply("Please enter the new FSUB_1 channel ID:")
    response = await client.listen(message.chat.id)
    fsub_1 = response.text
    
    await message.reply("Please enter the new FSUB_2 channel ID:")
    response = await client.listen(message.chat.id)
    fsub_2 = response.text
    
    await message.reply("Please enter the new FSUB_3 channel ID:")
    response = await client.listen(message.chat.id)
    fsub_3 = response.text
    
    await message.reply("Please enter the new FSUB_4 channel ID:")
    response = await client.listen(message.chat.id)
    fsub_4 = response.text
    
    # Save FSUB values to MongoDB
    save_fsub_data(fsub_1, fsub_2, fsub_3, fsub_4)
    
    # Reload the config and invitelinks
    reload_modules()
    
    await message.reply("FSUB values updated successfully!")

# Command: /show_fsub
@Client.on_message(filters.command('show_fsub') & filters.user(OWNER_ID) & filters.private)
async def show_fsub(client: Client, message: Message):
    # Reload config and invitelinks before displaying the latest values
    reload_modules()

    # Get the latest FSUB values from MongoDB
    fsub_1, fsub_2, fsub_3, fsub_4 = get_fsub_data()

    # Get invite links from invitelinks.py or fallback to bot.py if not available
    invitelinks = {
        'fsub_1': getattr(client, 'invitelink', None) if not hasattr(client, 'invitelink') else client.invitelink,
        'fsub_2': getattr(client, 'invitelink2', None) if not hasattr(client, 'invitelink2') else client.invitelink2,
        'fsub_3': getattr(client, 'invitelink3', None) if not hasattr(client, 'invitelink3') else client.invitelink3,
        'fsub_4': getattr(client, 'invitelink4', None) if not hasattr(client, 'invitelink4') else client.invitelink4
    }

    # Check if invitelinks are found in invitelinks.py, else fallback to bot.py
    if not invitelinks['fsub_1']:
        invitelinks['fsub_1'] = client.invitelink
    if not invitelinks['fsub_2']:
        invitelinks['fsub_2'] = client.invitelink2
    if not invitelinks['fsub_3']:
        invitelinks['fsub_3'] = client.invitelink3
    if not invitelinks['fsub_4']:
        invitelinks['fsub_4'] = client.invitelink4

    # Create the buttons with the FSUB values and their respective invite links
    buttons = [
        [InlineKeyboardButton(f"FSUB 1: {fsub_1}", url=invitelinks['fsub_1'])],
        [InlineKeyboardButton(f"FSUB 2: {fsub_2}", url=invitelinks['fsub_2'])],
        [InlineKeyboardButton(f"FSUB 3: {fsub_3}", url=invitelinks['fsub_3'])],
        [InlineKeyboardButton(f"FSUB 4: {fsub_4}", url=invitelinks['fsub_4'])]
    ]
    
    await message.reply(
        f"Current FSUB values:\n\nFSUB 1: {fsub_1}\nFSUB 2: {fsub_2}\nFSUB 3: {fsub_3}\nFSUB 4: {fsub_4}",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
