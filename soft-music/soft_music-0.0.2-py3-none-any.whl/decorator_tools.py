import time
import traceback
from functools import wraps


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

    def __init__(self, msg):
        self.msg = msg

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            import warnings
            warnings.simplefilter('always', DeprecationWarning)
            warnings.warn(
                "Call to deprecated method ({}({}):{}).{}".format
                (fn.__code__.co_filename.split('/')[-1],
                 fn.__code__.co_firstlineno,
                 fn.__name__, self.msg),
                category=DeprecationWarning,
                stacklevel=2)
            warnings.simplefilter('default', DeprecationWarning)  # reset filter
            return fn(*args, **kwargs)

        return wrapper
