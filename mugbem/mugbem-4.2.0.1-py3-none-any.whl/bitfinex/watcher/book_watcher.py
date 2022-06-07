from typing import Union

from . import base, processor


class BookWatcher(base.AbstractWatcher):
    def __init__(self, _processor: processor.AbstractProcessor):
        super(BookWatcher, self).__init__()
        self.processor = _processor

    def handle(self, message: Union[dict, list]):
        self.processor.handle(message)
