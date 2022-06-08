from cloudam_stream.core.ports.port import Port
from cloudam_stream.core.payload import Message, Record
from cloudam_stream.core.streams import RedisProducer
from cloudam_stream.core.utils import serialize_inner
from typing import TypeVar, Generic
import json


T = TypeVar("T")


class OutputPort(Generic[T], Port):
    def __init__(self, producer: RedisProducer = None, name=None, actor_name=None):
        if name and actor_name:
            self.channel = actor_name.replace(' ', '_') + '&' + name.replace(' ', '_')
        self.producer = producer
        super().__init__(name, actor_name)

    def encode(self, data: T):
        pass

    def emit(self, data: T):
        self._emit(data)

    def _emit(self, payload: T):
        message_object = Message(payload, "0", type(payload).__name__)
        print(json.dumps(message_object.__dict__))
        encode_msg = serialize_inner.encode(message_object)
        self.producer.produce(self.channel, encode_msg)


class TextOutputPort(OutputPort[str]):

    pass


class BinaryOutputPort(OutputPort[bytes]):

    pass


class IntOutputPort(OutputPort[int]):

    pass


class FloatOutputPort(OutputPort[float]):

    pass


class JsonOutputPort(OutputPort[dict]):

    pass


class RecordOutputPort(OutputPort[Record]):

    pass
