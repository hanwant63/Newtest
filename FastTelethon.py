from telethon import types

async def upload_file(client, file, name, progress_callback=None):
    return await client.send_file(client.chat_id, file=file, caption=name)
