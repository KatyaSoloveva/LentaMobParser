import os
import time
import hashlib
import uuid

from constants import CONSTANT_KET
from logger import logger


def generate_qrator_token(url, constant_key=CONSTANT_KET):
    url_path = url.split('?')[0]
    timestamp = str(int(time.time()))
    data = constant_key + url_path + timestamp
    md5_hash = hashlib.md5(data.encode('utf-8')).hexdigest()
    logger.info(f'Сгенерирован qrator_token: {md5_hash}')
    return md5_hash, timestamp


def generate_traceparent():
    version = '00'
    trace_id = os.urandom(16).hex()
    span_id = os.urandom(8).hex()
    flags = '01'
    traceparent = f'{version}-{trace_id}-{span_id}-{flags}'
    logger.info(f'Сгенерирован traceparent: {traceparent}')
    return traceparent


def generate_device_id():
    device_id = f'A-{uuid.uuid4()}'
    logger.info(f'Сгенерирован device_id: {device_id}')
    return device_id
