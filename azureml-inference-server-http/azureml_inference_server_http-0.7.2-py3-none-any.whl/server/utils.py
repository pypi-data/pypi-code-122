import contextlib
import os
import signal
import threading
import time
from types import FrameType, TracebackType
from typing import Iterator, Optional, Type


class Timer:
    __slots__ = ["start_time", "elapsed_ms"]

    def __enter__(self) -> "Timer":
        self.start_time = time.perf_counter()
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.elapsed_ms = (time.perf_counter() - self.start_time) * 1000


def timeout_supported() -> bool:
    # Signals are not supported on Windows and can only be used in the main thread.
    return os.name != "nt" and threading.current_thread() is threading.main_thread()


def _alarm_handler(signalnum: int, frame: Optional[FrameType]) -> None:
    raise TimeoutError


@contextlib.contextmanager
def timeout(timeout_ms: int) -> Iterator[None]:
    # TODO: if timeout is not supported, we should let the user know.
    if timeout_supported():
        timeout_s = timeout_ms / 1000  # millisecond to seconds

        old_handler = signal.signal(signal.SIGALRM, _alarm_handler)
        signal.setitimer(signal.ITIMER_REAL, timeout_s)

        try:
            yield
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old_handler)
    else:
        yield
