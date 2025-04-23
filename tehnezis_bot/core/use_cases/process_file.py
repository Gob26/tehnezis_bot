import re
import pandas as pd
import httpx
from lxml import html
from aiogram import types

from core.entities.repositories import CrawlingTargetRepository
from core.entities.schemas import CrawlingTargetCreate
from infrastructure.database.database import get_async_session

def clean_price(text):
    """Очищает строку цены"""
    digits = re.sub(r"[^\d]", "", str(text))
    return int(digits) if digits else 0

def normalize_url(url):
    """Добавлем http:// """
    if isinstance(url, str):
        url = url.strip()
        if url.startswith(("http://", "https://")):
            return url
        else:
            return "http://" + url
    return url

async def fetch_price_by_xpath(url: str, xpath: str) -> int:
    """Получает цену по URL и XPath"""
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
            tree = html.fromstring(response.text)
            elements = tree.xpath(xpath)
            
            print(f"Найдено {len(elements)} элементов: {xpath}")
            for i, el in enumerate(elements, 1):
                print(f"  {i}. {el.text_content().strip()}")
            
            if elements:
                price_text = elements[0].text_content().strip()
                print(f"Цена: {price_text}")
                return clean_price(price_text)
            else:
                print(f"XPath ничего не вернул: {xpath}")
                return 0
    except Exception as e:
        print(f"Ошибка при получении цены: {e}")
        return 0
    


async def process_excel_file(message: types.Message, file_path: str) -> None:
    """Обрабатывает Excel-файл и выполняет нормализацию данных"""
    try:
        df = pd.read_excel(file_path)
        
        required_columns = ["title", "url", "xpath"]
        if not all(col in df.columns for col in required_columns):
            await message.answer("Файл не содержит необходимые столбцы: title, url, xpath.")
            return
        
        df["url"] = df["url"].apply(normalize_url)
        
        if "price" in df.columns:
            df["price"] = df["price"].apply(clean_price)
            
        targets = []
        errors = []

        for index, row in df.iterrows():
            try:
                price = row.get("price")
                if pd.isna(price) or price == 0:
                    price = await fetch_price_by_xpath(row["url"], row["xpath"])
                else:
                    price = clean_price(price)

                target = CrawlingTargetCreate(
                    title=row["title"],
                    url=row["url"],
                    xpath=row["xpath"],
                    price=price
                )
                targets.append(target)
            except Exception as e:
                errors.append(f"Ошибка {index + 2}: {e}. Title={row['title']}, URL={row['url']}, XPath={row['xpath']}")
        
        if errors:
            error_message = "Найдены ошбки в файле:\n " + "\n".join(errors[:10])
            if len(errors) > 10:
                error_message += "\n..."
            await message.answer(error_message)
            return
        
        async for session in get_async_session():
            repository = CrawlingTargetRepository(session)
            await repository.create_many(targets)

        # Отправляем сообщение об успешной обработке
        saved_data = "\n".join([f"✅ {target.title}:(Цена: {target.price})" for target in targets])
        await message.answer(f"Файл успешно обработан. Найдено {len(df)} записей.\n\nДобавленные данные:\n{saved_data}")
        return df  # Возвращаем обработанный DataFrame для дальнейшего использования
        
    except Exception as e:
        await message.answer(f"Оошибка при обработке файла: {str(e)}")
        return None