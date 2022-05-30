import asyncio
from inspect import signature


class WS:
    """This is the python wrapper for the web socket that will be used here.
    """
    def __init__(self, robyn_object, endpoint) -> None:
        self.robyn_object = robyn_object
        self.endpoint = endpoint
        self.methods = {}

    def on(self, type):
        def inner(handler):
            if type not in ["connect", "close", "message"]:
                raise Exception(f"Socket method {type} does not exist")
            else:
                self.methods[type] = (handler, self._is_async(handler), self._num_params(handler))
                self.robyn_object.add_web_socket(self.endpoint, self)

        return inner

    def _num_params(self, handler):
        return len(signature(handler).parameters)

    def _is_async(self, handler):
        return asyncio.iscoroutinefunction(handler)

