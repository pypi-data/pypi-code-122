from typing import List, Any

from pyutter.core.primitive import Style, Widget


class Container(Widget):
    def __init__(self, children: List[Any], id=None, style: Style = None):
        super().__init__('div', children, id, style)


class Center(Container):
    def __init__(self, children: List[Any], id=None, style: Style = None):
        style = style if style is not None else Style()
        style['display'] = 'flex'
        style['justify-content'] = 'center'
        super().__init__(children, id, style)


class Column(Container):
    def __init__(self, children: List[Any], id=None, style: Style = None):
        style = style if style is not None else Style()
        style['display'] = 'flex'
        style['flex-direction'] = 'column'
        # style['justify-content'] = 'center'

        super().__init__(children, id, style)


class Row(Container):
    def __init__(self, children: List[Any], id=None, style: Style = None):
        style = style if style is not None else Style()
        style['display'] = 'flex'
        style['flex-direction'] = 'row'
        # style['justify-content'] = 'center'

        super().__init__(children, id, style)


class Grid(Container):
    def __init__(self, children: List[Any], id=None, style: Style = None):
        # trying out a different pattern
        style = style if style is not None else {}
        style = Style(
            gap='16px',
            display='flex',
            **{"flex-wrap": 'wrap', "justify-content": "center"},
            **style)

        super().__init__(children, id, style)


class Padding(Container):
    def __init__(self, children: List[Any], top: int = 0, right: int = 0, bottom: int = 0, left: int = 0):
        style = Style()
        style['padding'] = f'{top}px {right}px {bottom}px {left}px'

        super().__init__(children, style=style)

    @staticmethod
    def symmetric(children: List[Any], x: int = 0, y: int = 0):
        return Padding(children, y, x, y, x)

    @staticmethod
    def all(children: List[Any], pad: int = 0) -> Container:
        return Padding(children, pad, pad, pad, pad)


class Margin(Container):
    def __init__(self, children: List[Any], top: int = 0, right: int = 0, bottom: int = 0, left: int = 0):
        style = Style()
        style['margin'] = f'{top}px {right}px {bottom}px {left}px'

        super().__init__(children, style=style)

    @staticmethod
    def symmetric(children: List[Any], x: int = 0, y: int = 0):
        return Margin(children, y, x, y, x)

    @staticmethod
    def all(children: List[Any], margin: int = 0) -> Container:
        return Margin(children, margin, margin, margin, margin)


class Spacer(Container):
    def __init__(self, width: int = 0, height: int = 0):
        style = Style()
        style['width'] = f'{width}px'
        style['height'] = f'{height}px'

        super().__init__([], style=style)

    @staticmethod
    def percent(width: float = 0, height: float = 0):
        style = Style()
        style['width'] = f'{width}%'
        style['height'] = f'{height}%'
        return Container([], style=style)


class Expanded(Container):
    def __init__(self):
        style = Style()
        style['flex-grow'] = '100'

        super().__init__([], style=style)


class Stack(Container):
    def __init__(self, children: List[Any]):
        style = Style(display='flex', **{"justify-content": "center"})

        for x in children:
            x.style['position'] = 'absolute'
        super().__init__(children, style=style)
