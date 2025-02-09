from aiohttp import web
from plugins import web_server

import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
import pyrogram.utils
pyrogram.utils.MIN_CHANNEL_ID = -1009147483647

from config import API_HASH, API_ID, LOGGER, BOT_TOKEN, BOT_WORKERS, FSUB_1, FSUB_2, FSUB_3, FSUB_4, DB_CHANNEL, PORT

STORAGE_CHANNEL = -1002197279542  # Channel to store invite links

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={"root": "plugins"},
            workers=BOT_WORKERS,
            bot_token=BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        invite_links = {}

        async def get_invite_link(chat_id, key):
            try:
                link = (await self.get_chat(chat_id)).invite_link
                if not link:
                    await self.export_chat_invite_link(chat_id)
                    link = (await self.get_chat(chat_id)).invite_link
                invite_links[key] = link
            except Exception as e:
                self.LOGGER(__name__).warning(e)
                self.LOGGER(__name__).warning(f"Failed to export invite link for {chat_id}")
                sys.exit()

        if FSUB_1:
            await get_invite_link(FSUB_1, "FSUB_1")
        if FSUB_2:
            await get_invite_link(FSUB_2, "FSUB_2")
        if FSUB_3:
            await get_invite_link(FSUB_3, "FSUB_3")
        if FSUB_4:
            await get_invite_link(FSUB_4, "FSUB_4")

        try:
            db_channel = await self.get_chat(DB_CHANNEL)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/NocoFlux")

        invite_text = "\n".join([f"{key}: {link}" for key, link in invite_links.items()])
        storage_message = await self.send_message(STORAGE_CHANNEL, f"<b>Invite Links</b>\n\n{invite_text}")
        self.storage_message_id = storage_message.id

        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
