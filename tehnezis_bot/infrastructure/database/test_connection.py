import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy import text
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from infrastructure.config import DATABASE_URL

async def test_db_connection():
    try:
        engine = create_async_engine(DATABASE_URL)
        async with engine.connect() as connection:
            print("Подключение к БД успешно установлено!")
            result = await connection.execute(text("SELECT 1"))
            one = result.scalar_one()
            assert one == 1
            print("Тестовый запрос выполнен успешно.")
    except OperationalError as e:
        print(f"Ошибка подключения к БД: {e}")
    finally:
        if 'engine' in locals():
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_db_connection())