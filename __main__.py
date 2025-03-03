from . import *
from .config import *
from .worker import *
from telethon import events

LOGS.info("Starting...")

try:
    bot.start(bot_token=BOT_TOKEN)
except Exception as er:
    LOGS.error(f"Bot start error: {er}")

@bot.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    if event.sender_id != OWNER:
        await event.reply("**Sorry, you are not authorized!**")
        return
    await event.reply("Bot started!")

@bot.on(events.NewMessage(pattern="/setcode"))
async def setcode_handler(event):
    if event.sender_id != OWNER:
        await event.reply("**Sorry, you are not authorized!**")
        return
    try:
        new_code = event.text.split(" ", 1)[1]
        config.ffmpegcode = [new_code]
        await event.reply(f"FFmpeg code updated to: {new_code}")
    except IndexError:
        await event.reply("Please provide a new FFmpeg code.")

@bot.on(events.NewMessage(pattern="/getcode"))
async def getcode_handler(event):
    if event.sender_id != OWNER:
        await event.reply("**Sorry, you are not authorized!**")
        return
    await event.reply(f"Current FFmpeg code: {config.ffmpegcode[0]}")

@bot.on(events.NewMessage(events.NewMessage(pattern=r"(?i)(.mp4|.avi|.mov|.mkv)$")))
async def video_handler(event):
    await compress_video(event)

LOGS.info("Bot has started.")
with bot:
    bot.run_until_disconnected()
