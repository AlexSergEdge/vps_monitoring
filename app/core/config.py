import os

from dotenv import load_dotenv
from pathlib import Path


env_file = Path.cwd() / '.env'
load_dotenv(dotenv_path=env_file)


class AppSettings:
    APP_NAME: str = 'VPS Monitoring'
    APP_VERSION: str = '0.0.1'
    
    # Contents of .env file
    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_SERVER: str = os.getenv('POSTGRES_SERVER')
    POSTGRES_PORT: str = os.getenv('POSTGRES_PORT',5432)
    POSTGRES_DB: str = os.getenv('POSTGRES_DB')
    
    POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


settings = AppSettings()