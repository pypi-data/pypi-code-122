"""
Class defining a shared counters aggregator
"""

from functools import wraps

from .abstract import AbsractSharable


class Counter(AbsractSharable):
    """
    An object to store counters to share between package dependencies

    Attributes
    ----------
    _shared: dict
        shared keys + values
    _registered_ids: list
        Name of hooks registered
    _allowed_cycles: list
        Hook name allowed for cycles (dangerous)
    _warning_on_cycles: list
        Hook names without print a warning on cycles and stop without raising
        an error
    hook_chaine: list
        List of curently opened hooks
    _key_update: dict
        Dictionnary of hooked functions linked to a tag
    """

    def __init__(self):
        super().__init__()
        self._key_update = {}

    def increment(self, key: str, pad: int = 1):
        """
        Add pad to the curent key value

        Parameters
        ----------
        key: str
            The key/tag to access to the shared counter
        pad: int
            The value to add to the counter

        Raises
        ------
        ValueError
            Raised when the key isn't initialized
        """
        if key is None:
            raise ValueError("The key isn't defined")
        self.set(key, value=self.get(key) + pad)

    def decrement(self, key: str, pad: int = 1):
        """
        Remove pad to the curent key value

        Parameters
        ----------
        key: str
            The key/tag to access to the shared counter
        pad: int
            The value to substract to the counter

        Raises
        ------
        ValueError
            Raised when the key isn't initialized
        """
        if key is None:
            raise ValueError("The key isn't defined")
        self.set(key, value=self.get(key) - pad)

    def set(self, key: str, value: int = 0, single_set: bool = True):
        """
        Add or replace a shared couple key + value and update hooks if single_set is used

        Parameters
        ----------
        key: str
            The key/tag to name the counter
        value: int
            The initial value (default=0)
        single_set: bool
            Trigger hooks linked to the tag if True (default). This parameter
            has to be set to False when updating multiple tags before running a
            batch of hooks.

        Returns
        -------
        The key if a value change occured without hooks update

        Raises:
        -------
        TypeError
            The key has to be a str
        TypeError
            The value has to be an int
        """
        if not isinstance(key, str):
            raise TypeError("The key has to be a str")
        if not isinstance(value, int):
            raise TypeError("The value has to be an int")

        return self._set_update(key, value, single_set)

    def update(self, key):
        """
        Run every functions hooked on the key

        Parameters
        ----------
        key: str
            The key/tag to access to the shared counter

        Raises
        ------
        RecursionError
            Raised to prevent cyclic update
        """
        if key is not None and key in self._key_update:
            if key in self.hook_chaine:
                raise RecursionError(
                    "A cyclic key update occured for %s with the curent chain %s"
                    % (key, str(self.hook_chaine))
                )
            for conditionnal_runner in self._key_update[key]:
                self.hook_chaine.append(key)
                conditionnal_runner.run(self.get(key))
                self.hook_chaine.pop()

    def set_hook(
        self,
        function,
        args=None,
        kwargs=None,
        key=None,
        equal=None,
        lower_than=None,
        bigger_than=None,
        lower_or_equal_to=None,
        bigger_or_equal_to=None,
    ):
        """
        Define a new hook to trigger a function on key update. Every defined conditions
        (cf paramaters: equal ,lower_than, bigger_than, lower_or_equal_to, bigger_or_equal_to)
        have to be fulffiled to trigger the function.

        Parameters
        ----------
        function:
            The triggered function
        args: list
            The list of parameters given to the function
        kwargs: dict
            The dict of named parameters given to the function
        key: str
            The key/tag to trigger the function when updated
        equal: int
            The counter has to be equal to this value to trigger the hook
        lower_than: int
            The counter has to be lower than to this value to trigger the hook
        bigger_than: int
            The counter has to be bigger than to this value to trigger the hook
        lower_or_equal_to: int
            The counter has to be lower or equal to this value to trigger the hook
        bigger_or_equal_to: int
            The counter has to be bigger or equal to this value to trigger the hook

        Raises
        ------
        ValueError
            The key has to exists.
        """
        args = () if args is None else args
        kwargs = {} if kwargs is None else kwargs
        if key is None:
            raise ValueError("Please provide a key as a hook to reload the function")
        if key is not None:
            if key not in self._key_update or self._key_update[key] is None:
                self._key_update[key] = []
            self._key_update[key].append(
                Counter.ConditionnalRunner(
                    function,
                    args,
                    kwargs,
                    equal,
                    lower_than,
                    bigger_than,
                    lower_or_equal_to,
                    bigger_or_equal_to,
                )
            )

    def updatable(
        self,
        key=None,
        single_registering=True,
        equal=None,
        lower_than=None,
        bigger_than=None,
        lower_or_equal_to=None,
        bigger_or_equal_to=None,
        cycles_allowed=False,
        warning_on_cycles=False,
    ):
        """
        Decorator to define a function reloaded on key change
        If single_registering is True, the hook will be created only if not existing to prevent the
        creation every time the decorated function is run.

        WARNING: cycles_allowed allow cycles when True and increase the probability of infinite
        recursivity. It would be better to let the default value to False and change the workflow
        instead.

        Parameters
        ----------
        key: str
            The key/tag to trigger the function when updated
        single_registering: bool
            Block the creation of a new hook each time the decorated function is instanciated in the
            code. Default is True.
        equal: int
            The counter has to be equal to this value to trigger the hook
        lower_than: int
            The counter has to be lower than to this value to trigger the hook
        bigger_than: int
            The counter has to be bigger than to this value to trigger the hook
        lower_or_equal_to: int
            The counter has to be lower or equal to this value to trigger the hook
        bigger_or_equal_to: int
            The counter has to be bigger or equal to this value to trigger the hook
        cycles_allowed: bool
            Allowing cycles for this hook when True (can lead to infinite reccursivity)
        warning_on_cycles: bool
            Printing a warning instead of raising an error on cycle. Still block the cycle.
        """

        def decorator(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                # Registering a hook if allowed
                hook_key = Counter.create_hook_name(key, function)
                if not single_registering or hook_key not in self._registered_ids:
                    self.set_hook(
                        function,
                        args,
                        kwargs,
                        key,
                        equal,
                        lower_than,
                        bigger_than,
                        lower_or_equal_to,
                        bigger_or_equal_to,
                    )
                    self._register_hook_key(hook_key, cycles_allowed, warning_on_cycles)
                # Running the function for the first time
                return function(*args, **kwargs)

            return wrapper

        return decorator

    class ConditionnalRunner:
        """
        Defining threshold to allow hook execution

        Attributes
        ----------
        function:
            The triggered function
        args: list
            The list of parameters given to the function
        kwargs: dict
            The dict of named parameters given to the function
        equal: int
            The counter has to be equal to this value to trigger the hook
        lower_than: int
            The counter has to be lower than to this value to trigger the hook
        bigger_than: int
            The counter has to be bigger than to this value to trigger the hook
        lower_or_equal_to: int
            The counter has to be lower or equal to this value to trigger the hook
        bigger_or_equal_to: int
            The counter has to be bigger or equal to this value to trigger the hook
        """

        def __init__(
            self,
            function,
            args,
            kwargs,
            equal=None,
            lower_than=None,
            bigger_than=None,
            lower_or_equal_to=None,
            bigger_or_equal_to=None,
        ):
            """
            Parameters
            ----------
            function:
                The triggered function
            args: list
                The list of parameters given to the function
            kwargs: dict
                The dict of named parameters given to the function
            equal: int
                The counter has to be equal to this value to trigger the hook
            lower_than: int
                The counter has to be lower than to this value to trigger the hook
            bigger_than: int
                The counter has to be bigger than to this value to trigger the hook
            lower_or_equal_to: int
                The counter has to be lower or equal to this value to trigger the hook
            bigger_or_equal_to: int
                The counter has to be bigger or equal to this value to trigger the hook
            """
            self.function = function
            self.args = args
            self.kwargs = kwargs
            self.equal = equal
            self.lower_than = lower_than
            self.bigger_than = bigger_than
            self.lower_or_equal_to = lower_or_equal_to
            self.bigger_or_equal_to = bigger_or_equal_to

        def run(self, value):
            """
            Run the function if every expected thresholds are True

            Parameters
            ----------
            value: int
                The value to compare to trigger the function
            """
            if (
                (self.equal is None or self.equal == value)
                and (self.lower_than is None or self.lower_than > value)
                and (self.bigger_than is None or self.bigger_than < value)
                and (self.lower_or_equal_to is None or self.lower_or_equal_to >= value)
                and (self.bigger_or_equal_to is None or self.bigger_or_equal_to <= value)
            ):
                return self.function(*self.args, **self.kwargs)
