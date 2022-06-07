from __future__ import annotations
import os
import sys
import warnings
from os import PathLike
from typing import Any
from importlib import reload
from pyprojroot import here


def source(file: str, globals: dict[str, Any] = None, locals: dict[str, Any] = None) -> None:
    """Source a python file

    Source a given python file in the current (or given) context

    Parameters
    ----------
    file: str
        The file to source
    globals: dict[str, Any], optional
        A globals object, if not the one of the caller
    locals: dict[str, Any], optional)
        A locals object, if not the one of the caller
    """
    if globals is None:
        globals = sys._getframe(1).f_globals
    if locals is None:
        locals = sys._getframe(1).f_locals
    with open(file, "rb") as f:
        code = compile(f.read(), file, 'exec')
        exec(code, globals, locals)


def add_to_sys_path(location: str | PathLike[str], warn: bool = True) -> None:
    """Add a location to the system path for importing

    Parameters
    ----------
    location: str | PathLike[str]
        The path to add to sys.path
    warn: bool, optional
        Warn if the path to be added does not exist. Defaults to True.
    """
    if warn and not os.path.exists(location):
        warnings.warn("Path doesn't exist: {}".format(location))
    if isinstance(location, PathLike):
        location = location.__fspath__()
    if location not in sys.path:
        sys.path.append(location)


def remove_from_sys_path(location: str | PathLike[str]) -> None:
    """Remove a location from the system path

    Parameters
    ----------
    location: str | PathLike[str]
        The path to remove from sys.path
    """
    if isinstance(location, PathLike):
        location = location.__fspath__()
    sys.path.remove(location)


__all__ = ["here", "source", "add_to_sys_path", "remove_from_sys_path", "reload"]
