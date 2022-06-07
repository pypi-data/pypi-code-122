import json
from abc import abstractmethod, ABCMeta
from typing import Union
import rel as orel
import websocket

from .requests.base.abstract_request import AbstractRequest


class AbstractWatcher(metaclass=ABCMeta):
    class WSConnection(websocket.WebSocketApp):
        def __init__(self, watcher: 'AbstractWatcher'):
            super(AbstractWatcher.WSConnection, self).__init__(
                "wss://api-pub.bitfinex.com/ws/2",
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
                keep_running=True
            )
            self.watcher = watcher

        def on_message(self, _, message):
            self.watcher.handle(json.loads(message))

        def on_error(self, _, error):
            print(error)

        def on_close(self, ws, close_status_code, close_msg):  # noqa
            pass

        def on_open(self, ws):
            ws.send(self.watcher.request.to_json())

    def __init__(self):
        self.ws = None
        self.request = None

    def subscribe(self, request: AbstractRequest):
        self.request = request
        self.ws = AbstractWatcher.WSConnection(self)
        websocket.enableTrace(False)
        print('>>> Started Mugbem OSAS <<<')
        print('> ')
        print('> working..', flush=True)
        self.ws.run_forever()
        orel.signal(2, orel.abort)
        orel.dispatch()

    @abstractmethod
    def handle(self, message: Union[dict, list]):
        pass
