from gc import is_tracked
from sys import getsizeof
from psutil import virtual_memory
from itertools import repeat
from pointers import to_ptr, Pointer
from typing import Iterable, Type, Any, Callable


class Eat(Pointer):
    def __init__(self, obj: Type[Any]) -> Type[Pointer]:
        self.obj = obj
        self.its = 1
        Pointer.__init__(self, id(self.obj), type(self.obj), is_tracked(self.obj))

    @property
    def size(self):
        return getsizeof(self.obj)

    @property
    def memuse(self):
        return virtual_memory()

    def __iter__(self):
        return repeat(Pointer(id(self.obj), type(self.obj), is_tracked(self.obj)), self.its)

    def __enum__(self):
        return [pt for pt in self.__iter__()]

    def gen(self, method : Callable[[Iterable, Any], Any], its : int, compute = False, *args, **kwargs) -> Iterable:
        self.its =  its
        enum = self.__enum__()
        if not compute:
            return method(enum, *args, **kwargs)
        else:
            return method([(~pt) for pt in enum], *args, **kwargs)

    def __repr__(self):
        return f"""Cereal Pointer to:\n
                   PyObject: {self.type.__name__}\n
                   Address: {hex(self.address)}\n
                   Size: {self.size}"""

def eat(obj : Any, its : int,  method : Callable[[Iterable, Any], Any] = list, compute = False, *args: Any, **kwargs: Any) -> Type[Iterable]:
    """Create an iterable set of pointers to a specified length. Useful for parellelizing large
    datasets. Use simply to generate a list, or extensibly through custom methods which expect an iterator.
    Pass args or kwargs directly, for use when constructing the data with the method passed. If compute is False, to reaccess the value
    in the pointer, call `~` at computation time

    Args:
            obj : (Any) ->         PyObject to repeat over
            its : (int) ->         number of iterations
            method : Callable -> method / function which accepts the repeated object and structures it to the
                                            passed `args` & `kwargs`
            compute : (bool) ->    access items in pointer while constructing the data. delay computation and return 
                                    pointers if False, or calculate a structured repeated object if True (eg DataFrame)

    Returns: Callable -> list, array, etc.

    Eg.
    ```py
    import numpy as np
    from cereal import eat

    x = [1, 2, 3, 4]

    yum = eat(x, its = 4, method = np.array, copy = False)

    >> yum
    >> array([<pointer to list object at 0x113b3edc0>,
              <pointer to list object at 0x113b3edc0>,
              <pointer to list object at 0x113b3edc0>,
              <pointer to list object at 0x113b3edc0>], dtype=object) # 4 pointers to the original object

    >> (~yum[0])[0]
    >> 1

    yum[0][0] = 4

    >> x # the original object
    >> [4, 2, 3, 4] # it changed!
    ```
    DataFrame
    ```py
    import pandas as pd
    from cereal import eat

    x = [1, 2, 3, 4]

    yum = eat(x, its = 4, method = pd.DataFrame, compute=True, columns = ['a', 'b', 'c', 'd'])

    >> yum # outputs a dataframe with columns ['a', 'b', 'c', 'd'] with [1, 2, 3, 4] repeated 4x.

    ```
    """
    return Eat(obj).gen(method, its, compute, *args, **kwargs)

