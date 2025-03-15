import os

from dotenv import load_dotenv
from pathlib import Path


env_file = Path.cwd() / '.env'
load_dotenv(dotenv_path=env_file)


class MonitoringSettings:
    TELEGRAM_ACCESS_TOKEN = os.getenv("TELEGRAM_ACCESS_TOKEN")
    TELEGRAM_BOT_USERNAME = os.getenv("TELEGRAM_BOT_USERNAME")
    SERVERS_CONFIG = os.getenv("SERVERS_CONFIG")
    ALLOWED_USERS = os.getenv("ALLOWED_USERS").split(',')
    DEFAULT_CHECK_INTERVAL = os.getenv("DEFAULT_CHECK_INTERVAL")

    
    # These values can be overrided (for example - use in docker compose)
    KNOWN_HOSTS_PATH = os.getenv("KNOWN_HOSTS_PATH")
    KNOWN_HOSTS_APP_PATH = os.getenv("KNOWN_HOSTS_APP_PATH", KNOWN_HOSTS_PATH)
    
    SSH_KEYS_PATH = os.getenv("SSH_KEYS_PATH")
    SSH_KEYS_APP_PATH = os.getenv("SSH_KEYS_APP_PATH", SSH_KEYS_PATH)


settings = MonitoringSettings()