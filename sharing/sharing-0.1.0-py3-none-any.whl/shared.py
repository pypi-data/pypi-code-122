"""
Class defining a shared variable aggregator
"""
from functools import wraps

from .abstract import AbsractSharable
from .common import LOGGER


class Shared(AbsractSharable):
    """
    An object to store variables to share between package dependencies

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
    _file_update: dict
        Dictionnary of hooked functions linked to a file name
    _key_update: dict
        Dictionnary of hooked functions linked to a tag
    hook_chaine: list
        List of curently opened hooks
    """

    def __init__(self):
        super(Shared, self).__init__()
        self._file_update = {}
        self._key_update = {}

    def set(self, key: str, value, single_set: bool = True):
        """
        Add a shared couple key + value and update hooks if single_set is used

        Parameters
        ----------
        key: str
            The key/tag to name the shared variable
        value
            The shared variable
        single_set: bool
            Trigger hooks linked to the tag if True (default). This parameter
            has to be set to False when updating multiple tags before running a
            batch of hooks.

        Returns
        -------
        The key if a value change occured without hooks update

        Raises
        ------
        TypeError
            The key has to be a str
        """
        if not isinstance(key, str):
            raise TypeError("The key has to be a str")

        return self._set_update(key, value, single_set)

    def _lock_update(self, key: str, lock_value: bool):
        """
        Lock or unlock the value to avoid update

        Parameters
        ----------
        key: str
            The key/tag to name the shared variable
        lock_value: bool
            The lock status to apply

        Raises
        ------
        TypeError
            The key has to be a str
        ValueError
            Raised when the key isn't initialized
        """
        if not isinstance(key, str):
            raise TypeError("The key has to be a str")
        if key not in self._shared:
            raise ValueError("The key %s doesn't exists and can't be locked" % key)
        self._shared[key] = (self._shared[key][0], True)

    def lock(self, key: str):
        """
        Lock the value to avoid update

        Parameters
        ----------
        key: str
            The key/tag to lock
        """
        self._lock_update(key, True)

    def unlock(self, key: str):
        """
        Unlock the value to allow update

        Parameters
        ----------
        key: str
            The key/tag to unlock
        """
        self._lock_update(key, False)

    def _test_cycle_and_run_hook(self, function, args: list, kwargs: dict, key: str):
        """
        Prevent cyclic anallowed keys modification and run the function triggered

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

        Raises
        ------
        RecursionError
            Raised to prevent cyclic update
        """
        hook_name = Shared.create_hook_name(key, function)
        if key in self.hook_chaine:
            if hook_name not in self._allowed_cycles and hook_name not in self._warning_on_cycles:
                raise RecursionError(
                    "A cyclic key update occured for %s with the curent chain %s"
                    % (key, str(self.hook_chaine))
                )
            elif hook_name in self._warning_on_cycles:
                LOGGER.warning(
                    (
                        "Unallowed cyclic key update attempt for %s. The recursive key update "
                        + "propagation is stopped from %s."
                    )
                    % (key, hook_name)
                )
                return
        self.hook_chaine.append(key)
        function(*args, **kwargs)
        self.hook_chaine.pop()

    def update(self, key: str = None, filename: str = None):
        """
        Run every functions hooked on the key and the filename

        Parameters
        ----------
        key: str
            The key/tag to trigger the function when updated
        filename: str
            The filename to trigger the function when updated
        """
        if key is not None and key in self._key_update:
            for function, args, kwargs in self._key_update[key]:
                self._test_cycle_and_run_hook(function, args, kwargs, key)
        if filename is not None and filename in self._file_update:
            for function, args, kwargs in self._file_update[filename]:
                self._test_cycle_and_run_hook(function, args, kwargs, filename)

    def set_hook(self, function, args: list = None, kwargs: dict = None, key: str = None, filename: str = None):
        """
        Define a new hook to trigger a function on key or file update

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
        filename: str
            The filename to trigger the function when updated
        """
        args = () if args is None else args
        kwargs = {} if kwargs is None else kwargs
        if key is None and filename is None:
            raise ValueError("Please provide a key or a file as a hook to reload the function")
        if key is not None:
            if key not in self._key_update or self._key_update[key] is None:
                self._key_update[key] = []
            self._key_update[key].append((function, args, kwargs))
        if filename is not None:
            if self._file_update[filename] is None:
                self._file_update[filename] = []
            self._file_update[filename].append((function, args, kwargs))

    def updatable(
        self,
        key: str = None,
        filename: str = None,
        single_registering: bool = True,
        cycles_allowed: bool = False,
        warning_on_cycles: bool = False,
    ):
        """
        Decorator to define a function reloaded on key or filename change
        If single_registering is True, the hook will be created only if not existing to prevent the
        creation every time the decorated function is run.

        WARNING: cycles_allowed allow cycles when True and increase the probability of infinite
        recursivity. It would be better to let the default value to False and change the workflow
        instead.

        Parameters
        ----------
        key: str
            The key/tag to trigger the function when updated
        filename: str
            The filename to trigger the function when updated
        single_registering: bool
            Block the creation of a new hook each time the decorated function is instanciated in the
            code. Default is True.
        cycles_allowed: bool
            Allowing cycles for this hook when True (can lead to infinite reccursivity)
        warning_on_cycles: bool
            Printing a warning instead of raising an error on cycle. Still block the cycle.
        """

        def decorator(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                if cycles_allowed and warning_on_cycles:
                    raise ValueError(
                        "warning_on_cycle block the recursivity and therefore can't be used "
                        + "with cycles_allowed"
                    )
                # Distinct hook defined with the couple function name + key or filename
                hook_key = Shared.create_hook_name(key, function)
                hook_file = Shared.create_hook_name(filename, function)
                # Registering a hook if allowed
                if (
                    not single_registering
                    or hook_key not in self._registered_ids
                    or hook_file not in self._registered_ids
                ):
                    self.set_hook(function, args, kwargs, key, filename)
                    self._register_hook_key(hook_key, cycles_allowed, warning_on_cycles)
                    self._register_hook_key(hook_file, cycles_allowed, warning_on_cycles)
                # Running the function for the first time
                return function(*args, **kwargs)

            return wrapper

        return decorator
