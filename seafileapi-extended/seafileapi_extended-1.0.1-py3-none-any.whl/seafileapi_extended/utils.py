"""Utils"""
from functools import wraps

from seafileapi.exceptions import ClientHttpError, DoesNotExist


def raise_does_not_exist(msg):
    """Decorator to turn a function that get a http 404 response to a
    :exc:`DoesNotExist` exception."""
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ClientHttpError as e:
                if e.code == 404:
                    raise DoesNotExist(msg)
                else:
                    raise
        return wrapped
    return decorator


def is_ascii(text) -> bool:
    """Check if is ascii"""
    try:
        text.encode("ascii")
    except UnicodeEncodeError:
        return False
    return True
