"""
Class defining an abstract shared variable aggregator
"""


class AbsractSharable:
    """
    An abstract class to store variables to share between package dependencies

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
    """

    def __init__(self):
        self._shared = {}  # shared keys + values
        self._registered_ids = []  # Name of hooks registered
        self.hook_chaine = []  # List of curently opened hooks
        self._allowed_cycles = []  # hook name allowed for cycles (dangerous)
        self._warning_on_cycles = []  # No error on cycle but stop and print a warning

    def __str__(self):
        return "%s={shared_keys:{%s}, registered_hooks:{%s}}" % (
            self.__class__.__name__,
            ", ".join(self._shared.keys()),
            ", ".join(self._registered_ids),
        )

    def set(self, key: str, value, single_set: bool, *args, **kwargs):
        """
        Add a shared couple key + value and update hooks if single_set is used

        Parameters
        ----------
        key: str
            The key/tag to name the shared variable
        value
            The shared variable
        single_set: bool
            Trigger hooks linked to the tag if True (default). This parameter has to be set to
            False when updating multiple tags before running a batch of hooks.

        Raises
        ------
        NotImplementedError
            This is an abstract method
        """
        raise NotImplementedError("%s.set" % self.__class__.__name__)

    def _register_hook_key(self, hook_key: str, cycles_allowed: bool, warning_on_cycles: bool):
        """
        Register the hook key to manage known hooks, cycle allowed hooks and warning on cycles

        Parameters
        ----------
        hook_key: str
            A hook_key name generated from the function name and the key tag to target a hook
        cycles_allowed: bool
            Allowing cycles for this hook when True (can lead to infinite reccursivity)
        warning_on_cycles: bool
            Printing a warning instead of raising an error on cycle. Still block the cycle.
        """
        if hook_key is not None and hook_key not in self._registered_ids:
            self._registered_ids.append(hook_key)
            if cycles_allowed:
                self._allowed_cycles.append(hook_key)
            elif warning_on_cycles:
                self._warning_on_cycles.append(hook_key)

    def _set_update(self, key: str, value, single_set: bool):
        """
        Add a shared couple key + value without controle and update hooks if single_set is used

        Parameters
        ----------
        key: str
            The key/tag to name the shared variable
        value
            The shared variable
        single_set: bool
            Trigger hooks linked to the tag if True (default). This parameter has to be set to
            False when updating multiple tags before running a batch of hooks.

        Returns
        -------
        The key if a value change occured without hooks update

        Raises
        ------
        ValueError
            Raised when trying to update a key whom can't be updated
        """
        if key in self._shared:
            # The key exists
            if value == self._shared[key][0]:
                # No change, nothing to do
                return
            if self._shared[key][1]:
                # A locked value can't be updated
                raise ValueError("The key %s is locked" % key)

        self._shared[key] = (value, False)  # Updating or creating the key

        if single_set:
            # Applying the hooks if the set isn't part of a variable group change
            self.update(key=key)
        else:
            # Hooks not applied, the set is part of a variable group change, the key is returned
            # for futur hooks group update
            return key

    def get(self, key: str):
        """
        Search the shared value based on the given key and return it if existing or return None

        Parameters
        ----------
        key: str
            The key/tag to access to the shared variable

        Returns
        -------
        The value if existing or None

        Raises
        ------
        TypeError
            The key has to be a str
        """
        if not isinstance(key, str):
            raise TypeError("The config key has to be a str")
        return self._shared.get(key, (None, None))[0]

    def update(self, *args, **kwargs):
        """
        Run every functions hooked on the key and the filename

        Raises
        ------
        NotImplementedError
            This is an abstract method
        """
        raise NotImplementedError("%s.updatable" % self.__class__.__name__)

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

        Raises
        ------
        NotImplementedError
            This is an abstract method
        """
        raise NotImplementedError("%s.set_hook" % self.__class__.__name__)

    @staticmethod
    def create_hook_name(key: str, function):
        """
        Generate a hook name

        Parameters
        ----------
        key: str
            The key/tag name
        function:
            The triggered function
        """
        return None if key is None else "%s:%s" % (function.__name__, key)

    def updatable(self, *args, **kwargs):
        """
        Decorator to define a function reloaded on key or filename change

        Raises
        ------
        NotImplementedError
            This is an abstract method
        """
        raise NotImplementedError("%s.updatable" % self.__class__.__name__)
