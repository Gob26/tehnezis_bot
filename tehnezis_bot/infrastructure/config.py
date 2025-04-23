import os
from dotenv import load_dotenv

load_dotenv()

def get_required_env(key: str) -> str:
    value = os.getenv(key)
    if not value or value.strip() == "":
        raise ValueError(f"Переменная окружения {key} отсутствует или пуста!")
    return value

BOT_TOKEN = get_required_env("BOT_TOKEN")
DB_USER = get_required_env("DB_USER")
DB_PASSWORD = get_required_env("DB_PASSWORD")
DB_NAME = get_required_env("DB_NAME")
DB_HOST = get_required_env("DB_HOST")
DB_PORT = get_required_env("DB_PORT")

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
