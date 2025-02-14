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
            plugins={
                "root": "plugins"
            },
            workers=BOT_WORKERS,
            bot_token=BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        if FSUB_1:
            try:
                link = (await self.get_chat(FSUB_1)).invite_link
                if not link:
                    await self.export_chat_invite_link(FSUB_1)
                    link = (await self.get_chat(FSUB_1)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FSUB_1 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: FSUB_1}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/weebs_support for support")
                sys.exit()
        if FSUB_2:
            try:
                link = (await self.get_chat(FSUB_2)).invite_link
                if not link:
                    await self.export_chat_invite_link(FSUB_2)
                    link = (await self.get_chat(FSUB_2)).invite_link
                self.invitelink2 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FSUB_2 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FSUB_2}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/weebs_support for support")
                sys.exit()
        if FSUB_3:
            try:
                link = (await self.get_chat(FSUB_3)).invite_link
                if not link:
                    await self.export_chat_invite_link(FSUB_3)
                    link = (await self.get_chat(FSUB_3)).invite_link
                self.invitelink3 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FSUB_3 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FSUB_3}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/weebs_support for support")
                sys.exit()
        if FSUB_4:
            try:
                link = (await self.get_chat(FSUB_4)).invite_link
                if not link:
                    await self.export_chat_invite_link(FSUB_4)
                    link = (await self.get_chat(FSUB_4)).invite_link
                self.invitelink4 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FSUB_4 value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FSUB_4}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/weebs_support for support")
                sys.exit()
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the DB_CHANNEL Value, Current Value {DB_CHANNEL}")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/weebs_support for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/codeflix_bots")
        self.LOGGER(__name__).info(f"""       


  ___ ___  ___  ___ ___ _    _____  _____  ___ _____ ___ 
 / __/ _ \|   \| __| __| |  |_ _\ \/ / _ )/ _ \_   _/ __|
| (_| (_) | |) | _|| _|| |__ | | >  <| _ \ (_) || | \__ \
 \___\___/|___/|___|_| |____|___/_/\_\___/\___/ |_| |___/
                                                         
 
                                          """)
        self.username = usr_bot_me.username
        #web-response
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")