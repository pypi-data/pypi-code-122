"""
py3lite
======
A light weight sqlite3 ORM for humans

Provides
1. A Model base class you can inherit from to create diverse tables.
2. A Connection class that handles you database connection.
3. Lazy Query objects, dict factory, model factory, row factory
4. API for custom functions written in python
5. ForeinKey support and reverse look up
6. You can build your own Fields and plug them into the ORM.

Documentation
----------------------------
www.github.com/py3lite.git

SUBMODULES
    1. models

Available classes and modules
    1. py3lite.py3lite.connection.Connection
    2. py3lite.py3lite.decorators.multimethod
    3. py3lite.py3lite.models.Model
    4. py3lite.py3lite.signals.Signal

Source code:
https://github.com/abiiranathan/py3lite.git

Pull requests and Bug fixes are welcome!
"""

from . import models
from .db import Model
from .connection import Connection
from .decorators import multimethod, overload, migrate
from .signals import Signal


__all__ = ['models', 'Model', 'Connection',
           'multimethod', 'overload', 'Signal', 'migrate', 'RemoteConnection']
