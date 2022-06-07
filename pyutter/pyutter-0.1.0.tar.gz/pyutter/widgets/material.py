from typing import List, Any

from pyutter.widgets.layout import Container
from pyutter.core.primitive import Style, Widget


class Card(Container):
    def __init__(self, children: List[Any], id=None, style: Style = None):
        style = style if style is not None else Style()
        style['box-shadow'] = '0 4px 8px 0 rgba(0,0,0,0.2)'
        style['border-radius'] = '0px'
        style['background'] = 'white'

        super().__init__(children, id, style)


class Chip(Container):
    def __init__(self, children: List[Any], id=None, size: int = 32, style: Style = None):
        style = style if style is not None else Style()
        style['display'] = 'flex'
        style['padding'] = f'0 {size / 2}px'
        style['align-items'] = 'center'
        style['height'] = f'{size}px'
        style['line-height'] = f'{size}px'
        style['border-radius'] = f'{size / 2}px'
        style['background-color'] = '#f1f1f1'
        style['margin-bottom'] = '5px'
        style['margin-right'] = '5px'

        super().__init__(children, id, style)


class AppBar(Widget):
    def __init__(self, children: List[Any], id=None, style: Style = None):
        style = style if style is not None else Style()
        style['box-shadow'] = '0 4px 8px 0 rgba(0,0,0,0.2)'
        style['display'] = 'flex'
        style['height'] = f'64px'
        style['width'] = f'100%'
        style['background'] = 'white'
        style['min-width'] = 'auto'
        # style['position'] = 'fixed'

        # style['box-shadow']= "var(--bs-sm)"
        super().__init__('div', children, id, style)
