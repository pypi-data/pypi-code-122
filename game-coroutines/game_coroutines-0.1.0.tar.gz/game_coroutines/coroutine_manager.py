"""CoroutineManager module"""

class CoroutineManager:
    """A class that manage other coroutines. """
    MANAGER = None

    def __init__(self):
        self.current_time = 0
        self.coroutines = set()
        self.running_coroutines = set()

    @classmethod
    def start(cls):
        """Sets a new CoroutineManager as default manager. """
        cls.MANAGER = CoroutineManager()

    @classmethod
    def register(cls, coroutine):
        """Register a new coroutine on the default CoroutineManager """
        cls.MANAGER._register(coroutine)

    def _register(self, coroutine):
        """Adds a new coroutine to this manager

        and set it's start_time and end_time
        """
        coroutine.start_time = self.current_time + coroutine.delay
        coroutine.end_time = coroutine.start_time + coroutine.duration
        self.coroutines.add(coroutine)

    @classmethod
    def remove(cls, coroutine):
        """Register a coroutine from the default CoroutineManager """
        cls.MANAGER._remove(coroutine)

    def _remove(self, coroutine):
        """Stops and remove a corountine from to-run and running sets. """
        self.coroutines.discard(coroutine)
        self.running_coroutines.discard(coroutine)

    @classmethod
    def update(cls, delta_time):
        """Update the time passed on the default CoroutineManager. """
        cls.MANAGER._update(delta_time)

    def _update(self, delta_time):
        """Update the time passsed on this manager.

        This function also detect if a coroutines is starting or it's ending.
        """
        self.current_time += delta_time

        self._detect_starting_coroutines()

        for coroutine in self.running_coroutines:
            coroutine.update_progress(self.current_time)

        self._detect_finished_coroutines()

    def _detect_starting_coroutines(self):
        """Detects what coroutines are starting """
        starting_coroutines = set()
        for coroutine in self.coroutines:
            if coroutine.is_running(self.current_time):
                starting_coroutines.add(coroutine)

        for starting_coroutine in starting_coroutines:
            self._add_coroutine_to_running(starting_coroutine)

    def _add_coroutine_to_running(self, coroutine):
        """Add the coroutine to the running set """
        self.coroutines.discard(coroutine)
        self.running_coroutines.add(coroutine)

    def _detect_finished_coroutines(self):
        """Detects what coroutines are ending """
        finished_coroutines = set()
        for coroutine in self.running_coroutines:
            if coroutine.is_finished(self.current_time):
                finished_coroutines.add(coroutine)

        for finished_coroutine in finished_coroutines:
            self._remove_coroutine_from_running(finished_coroutine)

    def _remove_coroutine_from_running(self, coroutine):
        """Remove the coroutine from the running set """
        self.running_coroutines.discard(coroutine)
