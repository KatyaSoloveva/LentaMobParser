from logger import logger
from generation import generate_device_id
from api_requests import get_session_token, bind_session_and_store, get_data
from services import get_product_data, load_to_db
from constants import (CATEGORY, LIMIT, MOSCOW_ID, MOSCOW_FILENAME, OFFSET,
                       SPB_FILENAME, SPB_ID)


def main(store_id, limit=LIMIT, category_id=CATEGORY, offset=OFFSET):
    logger.info(f'Старт парсинга для магазина {store_id}')
    device_id = generate_device_id()
    session_id = get_session_token(device_id)
    bind_session_and_store(store_id, device_id, session_id)

    all_products = []

    while True:
        response = get_data(device_id, session_id, category_id, limit, offset)
        page_products = get_product_data(response, device_id, session_id)

        if not page_products:
            logger.info('Страницы с товарами закончились.')
            break
        all_products.extend(page_products)
        offset += limit

    if store_id == MOSCOW_ID:
        load_to_db(MOSCOW_FILENAME, all_products)
    else:
        load_to_db(SPB_FILENAME, all_products)


if __name__ == "__main__":
    main(MOSCOW_ID)
    main(SPB_ID)
