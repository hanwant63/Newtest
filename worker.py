import asyncio
import os
from telethon.utils import get_extension
from . import *
from .FastTelethon import upload_file

QUEUE = {}

async def compress_video(event):
    if event.media:
        file_path = await event.download_media()
        if file_path:
            QUEUE[event.id] = file_path
            await event.reply("Video added to queue.")
            await process_queue(event)

async def process_queue(event):
    if QUEUE:
        file_path = QUEUE.pop(event.id)
        try:
            output_file = f"{os.path.splitext(file_path)[0]}_compressed{get_extension(file_path)}"
            command = f"ffmpeg -i '{file_path}' {' '.join(config.ffmpegcode)} '{output_file}'"
            process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            await process.wait()

            if os.path.exists(output_file):
                await upload_file(event.client, open(output_file, 'rb'), os.path.basename(output_file))
                os.remove(file_path)
                os.remove(output_file)
            else:
                await event.reply("Compression failed.")
        except Exception as e:
            LOGS.error(f"Compression error: {e}")
            await event.reply("An error occurred during compression.")
