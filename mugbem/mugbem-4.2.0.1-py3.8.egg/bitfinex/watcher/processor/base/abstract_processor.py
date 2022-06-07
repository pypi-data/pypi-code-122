from abc import ABCMeta, abstractmethod


class AbstractProcessor(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def handle(self, *args, **kwargs):
        pass
