from pyrogram import Client
from config import FSUB_1, FSUB_2, FSUB_3, FSUB_4

async def generate_invite_links(client: Client):
    invite_links = {}

    async def get_invite(fsub, key):
        if fsub:
            try:
                link = (await client.get_chat(fsub)).invite_link
                if not link:
                    await client.export_chat_invite_link(fsub)
                    link = (await client.get_chat(fsub)).invite_link
                invite_links[key] = link
            except Exception:
                invite_links[key] = None

    await get_invite(FSUB_1, "invitelink")
    await get_invite(FSUB_2, "invitelink2")
    await get_invite(FSUB_3, "invitelink3")
    await get_invite(FSUB_4, "invitelink4")

    return invite_links
