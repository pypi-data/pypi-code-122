from typing import List, Any

from pyutter.core.primitive import Input, Style


class button(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class checkbox(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class color(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class date(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class datetime(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class email(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class file(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class hidden(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class image(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class month(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class number(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class password(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class radio(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class range(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class reset(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class search(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class submit(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class tel(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class text(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class time(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class url(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)


class week(Input):
    def __init__(self, children: List[Any] = None, id=None, style: Style = None):
        super().__init__(self.__class__.__name__, children, id, style)
