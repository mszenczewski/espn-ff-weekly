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
    if return_type is bool:
        if str.lower(value) == 'false':
            return False
        return True
    if return_type is list:
        value = value.replace('[', '')
        value = value.replace(']', '')
        value = value.replace(',', '')
        return str.split(value)
    raise ValueError('invalid config type')

