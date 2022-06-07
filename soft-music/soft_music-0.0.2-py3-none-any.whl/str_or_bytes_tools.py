import numpy as np


def to_str(str_or_bytes, encoding='utf-8'):
    return str_or_bytes.decode(encoding) if hasattr(str_or_bytes, 'decode') else str_or_bytes


def to_bytes(str_or_bytes, encoding='utf-8'):
    return str_or_bytes.encode(encoding) if hasattr(str_or_bytes, 'encode') else str_or_bytes


def random_sleep(minimum, scale, max_timeout=5):
    min(np.random.pareto(1) * scale + minimum, max_timeout)
