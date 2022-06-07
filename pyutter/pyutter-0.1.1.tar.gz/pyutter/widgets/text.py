from typing import List, Any

from pyutter.core.primitive import TextWidget, Style


class H1(TextWidget):
    def __init__(self, child: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, child, id, style)


class H2(TextWidget):
    def __init__(self, child: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, child, id, style)


class H3(TextWidget):
    def __init__(self, child: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, child, id, style)


class H4(TextWidget):
    def __init__(self, child: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, child, id, style)


class H5(TextWidget):
    def __init__(self, child: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, child, id, style)


class P(TextWidget):
    def __init__(self, child: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, child, id, style)


class Plain(TextWidget):
    def __init__(self, child: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, child, id, style)


class A(TextWidget):
    def __init__(self, child: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, child, id, style)
