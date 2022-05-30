import asyncio
from typing import Optional, Tuple

from opentelemetry.context import Context  # type: ignore
from opentelemetry.sdk.trace import TracerProvider  # type: ignore
from opentelemetry.sdk.trace import ReadableSpan, Span, SpanProcessor  # type: ignore
from opentelemetry.util._time import _time_ns  # type: ignore


class AsyncMultiSpanProcessor(SpanProcessor):
    """Implementation of class:`SpanProcessor` that forwards all received
    events to a list of span processors sequentially.

    The underlying span processors are called in sequential order as they were
    added.
    """

    def __init__(self):
        # use a tuple to avoid race conditions when adding a new span and
        # iterating through it on "on_start" and "on_end".
        self._span_processors = ()  # type: Tuple[SpanProcessor, ...]
        self._lock = asyncio.Lock()

    async def add_span_processor(self, span_processor: SpanProcessor) -> None:
        """Adds a SpanProcessor to the list handled by this instance."""
        async with self._lock:
            self._span_processors += (span_processor,)

    def on_start(
        self,
        span: Span,
        parent_context: Optional[Context] = None,
    ) -> None:
        for sp in self._span_processors:
            sp.on_start(span, parent_context=parent_context)

    def on_end(self, span: ReadableSpan) -> None:
        for sp in self._span_processors:
            sp.on_end(span)

    def shutdown(self) -> None:
        """Sequentially shuts down all underlying span processors."""
        for sp in self._span_processors:
            sp.shutdown()

    async def force_flush(self, timeout_millis: int = 30000) -> bool:
        """Sequentially calls force_flush on all underlying
        :class:`SpanProcessor`

        Args:
            timeout_millis: The maximum amount of time over all span processors
                to wait for spans to be exported. In case the first n span
                processors exceeded the timeout followup span processors will be
                skipped.

        Returns:
            True if all span processors flushed their spans within the
            given timeout, False otherwise.
        """
        deadline_ns = _time_ns() + timeout_millis * 1000000
        for sp in self._span_processors:
            current_time_ns = _time_ns()
            if current_time_ns >= deadline_ns:
                return False

            if not await sp.force_flush((deadline_ns - current_time_ns) // 1000000):
                return False

        return True


class AsyncTracerProvider(TracerProvider):
    initialized: bool = False

    async def add_span_processor(self, span_processor: SpanProcessor) -> None:
        await self._active_span_processor.add_span_processor(span_processor)

    async def force_flush(self, timeout_millis: int = 30000) -> bool:
        return await self._active_span_processor.force_flush(timeout_millis)
