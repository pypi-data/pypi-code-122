import logging
from random import getrandbits
from typing import Any, Callable, Dict, Optional, Tuple, Union

import aiormq
from aiormq import ChannelInvalidStateError
from pamqp.common import Arguments

from .abc import (
    AbstractExchange, AbstractIncomingMessage, AbstractQueueIterator,
    AbstractRobustQueue, ConsumerTag, TimeoutType,
)
from .exchange import ExchangeParamType
from .queue import Queue, QueueIterator


log = logging.getLogger(__name__)


class RobustQueue(Queue, AbstractRobustQueue):
    __slots__ = ("_consumers", "_bindings")

    _consumers: Dict[ConsumerTag, Dict[str, Any]]
    _bindings: Dict[Tuple[Union[AbstractExchange, str], str], Dict[str, Any]]

    @staticmethod
    def _get_random_queue_name() -> str:
        rnd = getrandbits(128)
        return "amq_%s" % hex(rnd).lower()

    def __init__(
        self,
        channel: aiormq.abc.AbstractChannel,
        name: Optional[str],
        durable: bool = False,
        exclusive: bool = False,
        auto_delete: bool = False,
        arguments: Arguments = None,
        passive: bool = False,
    ):

        super().__init__(
            channel=channel,
            name=name or self._get_random_queue_name(),
            durable=durable,
            exclusive=exclusive,
            auto_delete=auto_delete,
            arguments=arguments,
            passive=passive,
        )

        self._consumers = {}
        self._bindings = {}

    async def restore(self, channel: aiormq.abc.AbstractChannel) -> None:
        self.channel = channel
        await self.declare()
        bindings = tuple(self._bindings.items())
        consumers = tuple(self._consumers.items())

        for (exchange, routing_key), kwargs in bindings:
            await self.bind(exchange, routing_key, **kwargs)

        for consumer_tag, kwargs in consumers:
            await self.consume(consumer_tag=consumer_tag, **kwargs)

    async def bind(
        self,
        exchange: ExchangeParamType,
        routing_key: str = None,
        *,
        arguments: Arguments = None,
        timeout: TimeoutType = None,
        robust: bool = True
    ) -> aiormq.spec.Queue.BindOk:
        if routing_key is None:
            routing_key = self.name

        result = await super().bind(
            exchange=exchange, routing_key=routing_key,
            arguments=arguments, timeout=timeout,
        )

        if robust:
            self._bindings[(exchange, routing_key)] = dict(
                arguments=arguments,
            )

        return result

    async def unbind(
        self,
        exchange: ExchangeParamType,
        routing_key: str = None,
        arguments: Arguments = None,
        timeout: TimeoutType = None,
    ) -> aiormq.spec.Queue.UnbindOk:
        if routing_key is None:
            routing_key = self.name

        result = await super().unbind(
            exchange, routing_key, arguments, timeout,
        )
        self._bindings.pop((exchange, routing_key), None)

        return result

    async def consume(
        self,
        callback: Callable[[AbstractIncomingMessage], Any],
        no_ack: bool = False,
        exclusive: bool = False,
        arguments: Arguments = None,
        consumer_tag: ConsumerTag = None,
        timeout: TimeoutType = None,
        robust: bool = True,
    ) -> ConsumerTag:
        consumer_tag = await super().consume(
            consumer_tag=consumer_tag,
            timeout=timeout,
            callback=callback,
            no_ack=no_ack,
            exclusive=exclusive,
            arguments=arguments,
        )

        if robust:
            self._consumers[consumer_tag] = dict(
                callback=callback,
                no_ack=no_ack,
                exclusive=exclusive,
                arguments=arguments,
            )

        return consumer_tag

    async def cancel(
        self,
        consumer_tag: ConsumerTag,
        timeout: TimeoutType = None,
        nowait: bool = False,
    ) -> aiormq.spec.Basic.CancelOk:
        result = await super().cancel(consumer_tag, timeout, nowait)
        self._consumers.pop(consumer_tag, None)
        return result

    def iterator(self, **kwargs: Any) -> AbstractQueueIterator:
        return RobustQueueIterator(self, **kwargs)


class RobustQueueIterator(QueueIterator):
    async def consume(self) -> None:
        while True:
            try:
                return await super().consume()
            except ChannelInvalidStateError:
                await self._amqp_queue.channel.connection.ready()


__all__ = ("RobustQueue",)
