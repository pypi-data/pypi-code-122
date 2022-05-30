from functools import wraps
from . import db


def must_be_callable(func):
    """Function decorator that validates arguments for func"""

    @wraps(func)
    def inner(*args, **kwargs):
        sender = kwargs.get("sender") or args[1]
        receiver = kwargs.get("receiver") or args[2]

        # Sender must be a model instance
        if not issubclass(sender, db.Model):
            raise TypeError(
                f"sender should be a subclass of {type(db.Model)}! Got type {type(sender)}")

        if not callable(receiver):
            raise TypeError(
                f"receiver should be a callable! Got type {type(receiver)}")

        return func(*args, **kwargs)

    return inner


def validate(cls):
    """Class-decorator to validate hooks"""
    def __wrapper(*args, **kwargs):
        for name, func in vars(cls).items():
            if callable(func) and name.startswith("pre_") or name.startswith("post_"):
                return must_be_callable(func(*args, **kwargs))

            return func(*args, **kwargs)

    return __wrapper


@validate
class Signal(object):
    """
    Attach signals to models
    Each signal takes two arguments.

    sender: Model class to listen for the signal
    receiver: callback function. The model passes it's instance to the receiver
    """

    def pre_save(self, sender, receiver):
        setattr(sender, 'pre_save_callback', receiver)

    def post_save(self, sender, receiver):
        setattr(sender, 'post_save_callback', receiver)

    def pre_update(self, sender, receiver):
        setattr(sender, 'pre_update_callback', receiver)

    def post_update(self, sender, receiver):
        setattr(sender, 'post_update_callback', receiver)

    def pre_delete(self, sender, receiver):
        setattr(sender, 'pre_delete_callback', receiver)

    def post_delete(self, sender, receiver):
        setattr(sender, 'post_delete_callback', receiver)
