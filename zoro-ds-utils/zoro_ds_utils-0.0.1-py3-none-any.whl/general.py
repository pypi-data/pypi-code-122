"""Generic Python utilities."""
from typing import Any, Dict, List


def safe_nested_get(d: Dict, keys: List, default=None) -> Any:
    """Get a nested key's value from a dictionary.

    If the key doesn't exist, return `default` instead of raising a KeyError or TypeError.

    Args:
        d: A dictionary to search for 'keys'.
        keys: A list representing a nested dictionary key structure.
              E.g. safe_nested_get(d, keys=["a", "b", "c"] is a safe version of d["a"]["b"]["c"].
        default: The value to return if the nested `keys` structure doesn't exist in `d`.

    :Author: Zax Rosenberg
    """
    for key in keys:
        try:
            d = d[key]
        except (KeyError, TypeError):
            # KeyError: '<key>'
            # TypeError: '<type>' object is not subscriptable
            return default
    return d


def safe_nested_set(d: Dict, keys: List, value: Any) -> None:
    """Set a dictionary's `value` for a set of nested `keys`, inplace.

    If intermediate keys don't exist, they'll be created.
    In cases where `value` is a dictionary, and `keys` already exists,
    the previous value will be overwritten.
    To merge values instead, use `safe_nested_update`.

    Args:
        d: A dictionary to search for 'keys'.
        keys: A list representing a nested dictionary key structure.
              E.g. safe_nested_set(d, keys=["a", "b", "c"], "foo") is a safe version of d["a"]["b"]["c"] = "foo".
        value: The value to set.

    :Author: Zax Rosenberg
    """
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value


def safe_nested_update(d: Dict, updates: Dict) -> None:
    """Update a dictionary's contents with values from another nested dictionary, inplace.

    This method avoids overwriting the lowest level key when there are collisions, instead merging them.
    To overwrite on collisions, use `safe_nested_set`.

    Args:
        d: A dictionary to update with `updates`.
        updates: A dictionary from which to take values to add to `d`.

    :Author: Zax Rosenberg
    """
    for k, v in updates.items():
        if isinstance(v, dict):
            safe_nested_update(d.setdefault(k, {}), v)
        else:
            d[k] = v
