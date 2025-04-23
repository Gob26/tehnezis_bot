import httpx
from lxml import html

def fetch_price(url: str, xpath: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
        ),
        "Referer": "https://www.google.com/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ru,en-US;q=0.7,en;q=0.3",
        "Connection": "keep-alive"
    }

    try:
        with httpx.Client(headers=headers, timeout=10.0, follow_redirects=True) as client:
            response = client.get(url)
            response.raise_for_status()
            tree = html.fromstring(response.text)
            result = tree.xpath(xpath)
            if result:
                # Если результат — строка, возвращаем её
                if isinstance(result[0], str):
                    return result[0].strip()
                # Если результат — элемент, извлекаем его текст
                elif hasattr(result[0], 'text'):
                    return result[0].text.strip()
                else:
                    print(f"❌ Неизвестный тип результата: {type(result[0])}")
                    return ""
            else:
                print(f"❌ XPath ничего не вернул: {xpath}")
                return ""
    except httpx.HTTPStatusError as e:
        print(f"🚨 Ошибка при получении страницы: {e}")
        return ""
    except Exception as e:
        print(f"🚨 Общая ошибка: {e}")
        return ""

if __name__ == "__main__":
    url = "https://torg.1777.ru/one_board.php?board_poz_id=517387"
    xpath = "/html/body/div/div[2]/div[2]/table/tr/td[1]/div/div[1]/table/tr[1]/td[2]/span/span[1]"
    price = fetch_price(url, xpath)
    if price:
        print(f"💰 Цена: {price}")
    else:
        print("❌ Не удалось извлечь цену.")
