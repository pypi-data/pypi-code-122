"""Sequence module"""
from .coroutine_manager import CoroutineManager

class Sequence:
    """A Sequence holds an array of coroutines and call one after another. """
    def __init__(self, *coroutines):
        self.current_coroutine = 0
        self.coroutines = coroutines
        self._setup_callbacks()
        self()

    def __call__(self):
        if self.coroutines:
            self.coroutines[self.current_coroutine]()

    def _setup_callbacks(self):
        """Setup callbacks to call the next coroutine after ended. """
        self._remove_coroutines_from_manager()

        total_callbacks = len(self.coroutines)
        if total_callbacks <= 1:
            return

        for i in range(0, total_callbacks-1):
            original_callback = self.coroutines[i].callback

            def sequence_callback():
                if callable(original_callback):
                    original_callback()

                self.current_coroutine += 1
                self.coroutines[self.current_coroutine]()

            self.coroutines[i].callback = sequence_callback

    def _remove_coroutines_from_manager(self):
        """Remove all sequence coroutines from the ContentManager.

        This is necessary to setup the callbacks.
        """
        for coroutine in self.coroutines:
            CoroutineManager.remove(coroutine)
