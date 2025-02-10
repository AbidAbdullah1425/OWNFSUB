import base64
import re
import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from config import ADMINS, AUTO_DELETE_MS, AUTO_DELETE_MSG
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait

async def get_fsub_ids(client):
    try:
        # Fetch the message containing FSUB IDs
        message = await client.get_messages(-1002197279542, message_ids=[299])

        # Extract only FSUB IDs using regex
        fsub_ids = re.findall(r"-100\d{10}", message.text)

        # Convert extracted IDs to integers
        return [int(i) for i in fsub_ids]
    
    except Exception as e:
        print(f"Error fetching FSUB IDs: {e}")
        return []


async def is_subscribed(filter, client, update):
    fsub_ids = await get_fsub_ids(client)  # Fetch FSUB IDs dynamically

    if not fsub_ids:  # If no valid channel IDs
        return True

    user_id = update.from_user.id

    if user_id in ADMINS:
        return True

    member_status = [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]

    for channel_id in fsub_ids:
        try:
            member = await client.get_chat_member(chat_id=channel_id, user_id=user_id)
        except UserNotParticipant:
            return False

        if member.status not in member_status:
            return False

    return True


async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    return (base64_bytes.decode("ascii")).strip("=")


async def decode(base64_string):
    base64_string = base64_string.strip("=")
    base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
    return base64.urlsafe_b64decode(base64_bytes).decode("ascii")


async def get_messages(client, message_ids):
    messages = []
    total_messages = 0
    while total_messages != len(message_ids):
        temp_ids = message_ids[total_messages:total_messages + 200]
        try:
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temp_ids
            )
        except FloodWait as e:
            await asyncio.sleep(e.x)
            msgs = await client.get_messages(
                chat_id=client.db_channel.id,
                message_ids=temp_ids
            )
        except:
            pass
        total_messages += len(temp_ids)
        messages.extend(msgs)
    return messages


async def get_message_id(client, message):
    if message.forward_from_chat and message.forward_from_chat.id == client.db_channel.id:
        return message.forward_from_message_id
    elif message.forward_sender_name or not message.text:
        return 0

    pattern = r"https://t.me/(?:c/)?(.*)/(\d+)"
    matches = re.match(pattern, message.text)
    if not matches:
        return 0

    channel_id, msg_id = matches.groups()
    msg_id = int(msg_id)

    if channel_id.isdigit():
        if f"-100{channel_id}" == str(client.db_channel.id):
            return msg_id
    elif channel_id == client.db_channel.username:
        return msg_id

    return 0


def get_readable_time(seconds: int) -> str:
    time_units = ["s", "m", "h", "days"]
    time_list = []

    for i in range(4):
        seconds, result = divmod(seconds, 60 if i < 2 else 24)
        if seconds == 0 and result == 0:
            break
        time_list.append(f"{int(result)}{time_units[i]}")

    if len(time_list) == 4:
        return f"{time_list.pop()}, " + ":".join(reversed(time_list))

    return ":".join(reversed(time_list))


async def delete_file(messages, client, process):
    await asyncio.sleep(AUTO_DELETE_MS)
    for msg in messages:
        try:
            await client.delete_messages(chat_id=msg.chat.id, message_ids=[msg.id])
        except Exception as e:
            await asyncio.sleep(e.x)
            print(f"Failed to delete message {msg.id}: {e}")

    await process.edit_text(AUTO_DELETE_MSG)


subscribed = filters.create(is_subscribed)
