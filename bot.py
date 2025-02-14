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

        for i, fsub in enumerate([FSUB_1, FSUB_2, FSUB_3, FSUB_4], start=1):
            if fsub:
                try:
                    link = (await self.get_chat(fsub)).invite_link
                    if not link:
                        await self.export_chat_invite_link(fsub)
                        link = (await self.get_chat(fsub)).invite_link
                    setattr(self, f"invitelink{i}", link)
                except Exception as a:
                    self.LOGGER(__name__).warning(a)
                    self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                    self.LOGGER(__name__).warning(
                        f"Please Double check the FSUB_{i} value and Make sure Bot is Admin in channel "
                        f"with Invite Users via Link Permission, Current Force Sub Channel Value: {fsub}"
                    )
                    self.LOGGER(__name__).info("\nBot Stopped. Reach https://t.me/NocoFlux")
                    sys.exit()

        try:
            db_channel = await self.get_chat(DB_CHANNEL)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(
                f"Make sure bot is Admin in DB Channel, and Double check the DB_CHANNEL value, "
                f"Current Value: {DB_CHANNEL}"
            )
            self.LOGGER(__name__).info("\nBot Stopped. Reach https://t.me/NocoFlux")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"""[Force Sub Channels]
FSUB_1: {FSUB_1}
FSUB_2: {FSUB_2}
FSUB_3: {FSUB_3}
FSUB_4: {FSUB_4}
""")
        self.LOGGER(__name__).info("Bot Running..!\n\nCreated by \nhttps://t.me/NocoFlux")
        self.LOGGER(__name__).info("Bot is Good")
        self.username = usr_bot_me.username

        # Web response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
