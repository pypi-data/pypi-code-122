import json
from abc import ABCMeta, abstractmethod
from copy import deepcopy


class AbstractRequest(metaclass=ABCMeta):
    def __init__(self):
        self.request = {
            'event': 'subscribe'
        }

    @abstractmethod
    def get_channel(self) -> str:
        pass

    @abstractmethod
    def get_params(self) -> dict:
        pass

    def to_json(self, **json_params):
        self.request.update({
            'channel': self.get_channel(),
            **self.get_params()
        })
        return json.dumps(deepcopy(self.request), **json_params)
