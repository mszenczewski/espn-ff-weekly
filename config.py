import json
from typing import Optional
import configparser


CONFIG = configparser.RawConfigParser()
CONFIG.read(r'config.txt')


def get_config(header: str, key: str, return_type: Optional[type] = str):
    value = CONFIG.get(header, key)
    if return_type is str:
        return str(value)
    if return_type is int:
        return int(value)
    if return_type is list or bool:
        return json.loads(value)
    raise ValueError('invalid config type')

