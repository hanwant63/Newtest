import logging
from logging.handlers import RotatingFileHandler
from telethon import TelegramClient
from .config import *

LOG_FILE_NAME = "TG-videoCompress@Log.txt"

if os.path.exists(LOG_FILE_NAME):
    with open(LOG_FILE_NAME, "r+") as f_d:
        f_d.truncate(0)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=2097152000, backupCount=10),
        logging.StreamHandler(),
    ],
)
LOGS = logging.getLogger(__name__)

try:
    bot = TelegramClient(None, APP_ID, API_HASH)
except Exception as e:
    LOGS.error(f"Environment vars are missing: {e}")
    exit(1)
