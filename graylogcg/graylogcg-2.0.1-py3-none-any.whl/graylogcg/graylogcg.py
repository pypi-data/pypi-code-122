import logging
import graypy
from typing import AnyStr, Iterable, Dict, Optional, Any


class GraylogCG:
    def __init__(self, facility: str = AnyStr, host: str = AnyStr, tls: int = Iterable, payload: dict = Dict,
                 function: str = AnyStr, request: Any = Optional, response: Any = Optional):
        self.facility = facility
        self.host = host
        self.tls = tls
        self.payload = payload
        self.function = function
        self.request = request
        self.response = response

    def log_config(self):
        my_logger = logging.getLogger(self.facility)
        my_logger.setLevel(logging.DEBUG)

        handler = graypy.GELFTLSHandler(self.host, self.tls)
        my_logger.addHandler(handler)
        return my_logger

    def insert_log(self):
        try:
            my_logger = self.log_config()
            payload = {
                "request": self.request,
                "response": self.response,
            }
            payload.update(self.payload)
            my_logger.debug(msg=self.function, extra=payload)
            return {"status_log": True}
        except Exception as exc:
            return {"status_log": False, "except": exc}

    def insert_exception_log(self, exception: str = Optional, traceback: str = Optional):
        try:
            my_logger = self.log_config()
            payload = {
                "request": self.request,
                "response": self.response,
                "exception": exception,
                "traceback": traceback
            }
            my_logger.debug(msg=self.function, extra=payload.update(self.payload))
            return {"status_log": True}
        except Exception as exc:
            return {"status_log": False, "except": exc}
