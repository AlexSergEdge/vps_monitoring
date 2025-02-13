import os

from dotenv import load_dotenv
from pathlib import Path


env_file = Path.cwd() / '.env'
load_dotenv(dotenv_path=env_file)


class MonitoringSettings:
    # NOTE: taken fron .env file
    TELEGRAM_ACCESS_TOKEN = os.getenv("TELEGRAM_ACCESS_TOKEN")
    TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # This can be changed to group or personal chat
    SERVERS_CONFIG = os.getenv("SERVERS_CONFIG")

settings = MonitoringSettings()