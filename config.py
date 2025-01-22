import os
import logging
import redis
from logging.handlers import RotatingFileHandler
from pymongo import MongoClient
from bson import ObjectId

# Mandatory Environment Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7438884533:AAGUCrHeOxpBJrXXu3PTyrkWPirgYkwbuIc")
API_ID = int(os.environ.get("API_ID", "26254064"))
API_HASH = os.environ.get("API_HASH", "72541d6610ae7730e6135af9423b319c")
AUTO_DELETE = os.environ.get("AUTO_DELETE", True)
AUTO_DELETE_MS = int(os.environ.get("AUTO_DELETE_MS", "600"))
AUTO_DELETE_MSG = os.environ.get("AUTO_DELETE_MSG", "File WILL be DELETED in 10 minutes")
DB_CHANNEL = int(os.environ.get("DB_CHANNEL", "-1002279496397"))
OWNER_ID = int(os.environ.get("OWNER_ID", "5296584067"))
PORT = os.environ.get("PORT", "8080")
DB_URL = os.environ.get("DB_URL", "mongodb+srv://teamprosperpay:AbidAbdullah199@cluster0.z93fita.mongodb.net/")
DB_NAME = os.environ.get("DB_NAME", "Cluster0")

# MongoDB Client Setup
client = MongoClient(DB_URL)
db = client[DB_NAME]
collection = db["settings"]

# Redis Configuration
REDIS_HOST = os.environ.get("REDIS_HOST", "redis-17680.c232.us-east-1-2.ec2.redns.redis-cloud.com:17680")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "17680"))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "OvQhflEV6b8yu6OJMHo2eynM8XR0GJJC")

# Connect to Redis
redis_client = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True  # Ensures data is returned as strings
)

# Function to Fetch FSUB Variables from Redis
def update_fsub_values():
    global FSUB_1, FSUB_2, FSUB_3, FSUB_4
    FSUB_1 = int(redis_client.get("FSUB_1") or "-1002315395252")
    FSUB_2 = int(redis_client.get("FSUB_2") or "-1002386614375")
    FSUB_3 = int(redis_client.get("FSUB_3") or "-1002253609533")
    FSUB_4 = int(redis_client.get("FSUB_4") or "-1002386614375")

# Call `update_fsub_values` Whenever FSUB Values Are Needed
update_fsub_values()

BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))
START_PIC = os.environ.get("START_PIC", "https://envs.sh/_BZ.jpg")
START_MSG = os.environ.get("START_MESSAGE", "Hello {first} I'm a bot who can store files and share it via special links")
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

ADMINS.append(OWNER_ID)
ADMINS.append(5296584067)

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

# Log Updated FSUB Values
LOGGER("ForceSub").info(f"FSUB_1={FSUB_1}, FSUB_2={FSUB_2}, FSUB_3={FSUB_3}, FSUB_4={FSUB_4}")
