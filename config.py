import os
import logging
import importlib
import pymongo, os
from logging.handlers import RotatingFileHandler
from pymongo import MongoClient
from bson import ObjectId

# Mandatory Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7438884533:AAGVoXpBJrXXu3PTyrkWPirgYkwbuIc")
API_ID = int(os.environ.get("API_ID", "26254064"))
API_HASH = os.environ.get("API_HASH", "72541d6610ae7730e6135af9423b319c")

# Auto-delete settings
AUTO_DELETE = os.environ.get("AUTO_DELETE", True)
AUTO_DELETE_MS = int(os.environ.get("AUTO_DELETE_MS", "600"))
AUTO_DELETE_MSG = os.environ.get("AUTO_DELETE_MSG", "File WILL be DELETED in 10 minutes")

# Database & Owner Config
DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002279496397"))
OWNER_ID = int(os.environ.get("OWNER_ID", "5296584067"))
PORT = os.environ.get("PORT", "8080")
DB_URL = os.environ.get("DB_URL", "mongodb+srv://teamprosperpay:AbidAbdullah199@cluster0.z93fita.mongodb.net/")
DB_NAME = os.environ.get("DB_NAME", "Cluster0")

# Telegram Bot Workers
BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
START_PIC = os.environ.get("START_PIC", "https://envs.sh/_BZ.jpg")
START_MSG = os.environ.get("START_MESSAGE", "Hello {first} I'm a bot who can store files and share it via special links")

# Admins
try:
    ADMINS = []
    for x in (os.environ.get("ADMINS", "5296584067").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.") 

FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "You have to join our Channels First")
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

dbclient = pymongo.MongoClient(DB_URL)
database = dbclient[DB_NAME]
user_data = database['users']


# Function to fetch FSUB values from MongoDB
def get_fsub(var_name, default_value):
    data = database["fsub"].find_one({"_id": var_name})
    return data["value"] if data else default_value

FSUB_1 = get_fsub("FSUB_1", "-1001234567890")
FSUB_2 = get_fsub("FSUB_2", "-1009876543210")
FSUB_3 = get_fsub("FSUB_3", "-1001122334455")
FSUB_4 = get_fsub("FSUB_4", "-1005566778899")

ADMINS.append(OWNER_ID)
ADMINS.append(5296584067)

# Logging Configuration
LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

LOGGER("ForceSub").info(f"FSUB_1={FSUB_1}, FSUB_2={FSUB_2}, FSUB_3={FSUB_3}, FSUB_4={FSUB_4}")


importlib.reload(importlib.import_module("config"))
