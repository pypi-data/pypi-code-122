import time
import traceback
import numpy as np
from functools import wraps


def to_str(str_or_bytes, encoding='utf-8'):
    return str_or_bytes.decode(encoding) if hasattr(str_or_bytes, 'decode') else str_or_bytes


def to_bytes(str_or_bytes, encoding='utf-8'):
    return str_or_bytes.encode(encoding) if hasattr(str_or_bytes, 'encode') else str_or_bytes


def random_sleep(minimum, scale, max_timeout=5):
    min(np.random.pareto(1) * scale + minimum, max_timeout)


def catch(do_catch=True, exceptions=TypeError, do_raise=None, prt_tb=False, skip_log=False):
    def dec(fn):
        @wraps(fn)
        def wrapper_(*args, **kwargs):
            if not do_catch:
                return fn(*args, **kwargs)
            try:
                return fn(*args, **kwargs)
            except exceptions as e:
                if not skip_log:
                    if prt_tb:
                        traceback.print_exc()
                if do_raise:
                    raise do_raise()

        return wrapper_

    return dec


def retry(tries=3, delay=0, back_off=1, raise_msg='', accepted=None):
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            max_tries, max_delay = tries, delay
            while max_tries > 0:
                rv = f(*args, **kwargs)
                if rv:
                    return rv
                max_tries -= 1
                time.sleep(1)
            else:
                if raise_msg:
                    raise Exception(raise_msg)
                return

        return f_retry  # true decorator -> decorated function

    return deco_retry  # @retry(arg[, ...]) -> true decorator

class Deprecated(object):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used.

    - It accepts a single parameter ``msg`` which is shown with the warning.
    - It should contain information which function or method to use instead.

    """

    def __init__(self, msg):
        self.msg = msg

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if cfg.get('cc.show_deprecated', False):
                import warnings
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(Y.format(
                    "Call to deprecated method ({}({}):{}).{}".format
                    (fn.__code__.co_filename.split('/')[-1],
                     fn.__code__.co_firstlineno,
                     fn.__name__, self.msg),
                    category=DeprecationWarning,
                    stacklevel=2))
                warnings.simplefilter('default', DeprecationWarning)  # reset filter
            return fn(*args, **kwargs)

        return wrapper