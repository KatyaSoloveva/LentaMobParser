import requests
from requests.exceptions import RequestException
import time

from generation import generate_qrator_token, generate_traceparent
from constants import BASE_URL, HEADERS
from logger import logger


def get_session_token(device_id):
    url = f'{BASE_URL}/auth/session/guest/token'
    q_token, timestamp = generate_qrator_token(url)
    headers = {
        **HEADERS,
        "Timestamp": timestamp,
        "Qrator-Token": q_token,
        "DeviceId": device_id,
    }
    try:
        response = requests.get(url, headers=headers)
        session_token = response.json().get('sessionId')
        logger.info('Получен сессионный токен')
        return session_token
    except RequestException as e:
        logger.critical(f'Ошибка получения сессионный токена: {e}')


def bind_session_and_store(store_id, device_id, session_id):
    url = f'{BASE_URL}/stores/pickup/{store_id}'
    q_token, timestamp = generate_qrator_token(url)
    traceparent = generate_traceparent()

    headers = {
        **HEADERS,
        "traceparent": traceparent,
        "Timestamp": timestamp,
        "Qrator-Token": q_token,
        "DeviceId": device_id,
        "SessionToken": session_id,
    }

    try:
        requests.put(url, headers=headers)
        logger.info(f'Успешная привязка сессии к магазину {store_id}')
    except RequestException as e:
        logger.critical(f'Ошибка привязки суссии к '
                        f'магазину {store_id}: {e}')


def get_brand(product_id, device_id, session_id, retries):
    url = f'{BASE_URL}/catalog/items/{product_id}'
    q_token, timestamp = generate_qrator_token(url)
    traceparent = generate_traceparent()

    headers = {
        **HEADERS,
        "traceparent": traceparent,
        "Timestamp": timestamp,
        "Qrator-Token": q_token,
        "DeviceId": device_id,
        "SessionToken": session_id,
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 429:
            if retries > 0:
                logger.warning(f'Превышен лимит запросов для эндпоинта {url}, '
                               f'пауза 5 сек, попыток осталось: {retries}')
                time.sleep(5)
                return get_brand(product_id, device_id, session_id,
                                 retries - 1)
            else:
                logger.error(f'Превышено максимальное количество попыток '
                             f'запроса на эндпоинт {url}')
                return None

        attributes = response.json().get('attributes', [])
        brand = next(
            (attr['value'] for attr in attributes if
             attr.get('alias') == 'brand'),
            None
        )
        logger.info(f'Получен бренд для {product_id}')
        return brand

    except RequestException as e:
        logger.critical(f'Ошибка при получении бренда для {product_id}: {e}')


def get_data(device_id, session_id, category_id, limit, offset):
    url = f'{BASE_URL}/catalog/items'
    q_token, timestamp = generate_qrator_token(url)
    traceparent = generate_traceparent()

    headers = {
        **HEADERS,
        "traceparent": traceparent,
        "Timestamp": timestamp,
        "Qrator-Token": q_token,
        "DeviceId": device_id,
        "SessionToken": session_id,
    }

    data = {
        'categoryId': category_id,
        'filters': {
            'multicheckbox': [],
            'checkbox': [],
            'range': []
        },
        'sort': {
            'type': 'popular',
            'order': 'desc'
        },
        'limit': limit,
        'offset': offset
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except RequestException as e:
        logger.critical(f'Ошибка при получении данных о товарах: {e}')
