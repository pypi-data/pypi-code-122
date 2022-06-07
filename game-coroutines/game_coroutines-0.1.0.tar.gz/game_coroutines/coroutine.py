"""Coroutine module"""
from .coroutine_manager import CoroutineManager

class Coroutine:
    """A class to represent a coroutine.

    Coroutine holds information to run a piece of code over time.
    """

    def __init__(self,
                 delay=0.0,
                 duration=0.3,
                 progress_func=None,
                 property_to_lerp=None,
                 from_value=None,
                 callback=None):
        self.progress_func = progress_func
        self.delay = delay
        self.duration = duration
        self.start_time = 0
        self.end_time = 0
        self.callback = callback
        self.called_callback = False

    def __call__(self):
        """Add this coroutine to the default CoroutineManager """
        CoroutineManager.register(self)

    def is_running(self, current_time):
        """Check if the coroutine is running.

        Returns True or False
        """
        return current_time >= self.start_time

    def is_finished(self, current_time):
        """Check if the coroutine is finished.

        Returns True or False
        """
        return current_time >= self.end_time

    def update_progress(self, current_time):
        """Function to called every FPS tick

        so it can update the progress_func and call callbacks if it ended.
        """
        total = self.end_time - self.start_time
        current = current_time - self.start_time
        run_percentage = current / total

        if run_percentage > 1:
            run_percentage = 1

        if callable(self.progress_func):
            self.progress_func(run_percentage)

        should_call_callback = run_percentage >= 1 and not self.called_callback
        if should_call_callback and callable(self.callback):
            self.callback()
