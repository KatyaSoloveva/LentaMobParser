import csv

from logger import logger
from api_requests import get_brand


def get_brands(response):
    filters = response.get('filters', {}).get('multicheckbox', [])
    brand_filter = next(
        (f for f in filters if f.get('attributeId') == 238),
        None
    )
    if brand_filter:
        return [brand['value'] for brand in brand_filter.get('values', [])]
    return []


def get_product_data(response, device_id, session_id):
    brands = get_brands(response)
    products = []
    items = response.get('items', [])

    for item in items:
        if item.get('count', 0) > 0:
            item_id = item.get('id', '')
            name = item.get('name', '')
            regular_price = item.get('prices', {}).get('costRegular', 0) / 100
            promo_price = item.get('prices', {}).get('cost', 0) / 100
            brand = next((b for b in brands if b in name), None)
            brand = get_brand(
                item_id, device_id, session_id, retries=3
            ) if not brand else brand
            products.append((item_id, name, f'{regular_price} руб.',
                             f'{promo_price:} руб.',  brand))

    return products


def load_to_db(filename, items):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(('id', 'Наименование', 'Регулярная цена',
                             'Промо цена', 'Бренд'))
            writer.writerows(items)
            logger.info(f'Данные успешно записаны в файл: {filename}')
    except Exception as e:
        logger.error(f'Ошибка при записи данных в файл {filename}: {e}')
