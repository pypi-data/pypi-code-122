from typing import List, Any

from pyutter.core.primitive import ButtonWidget, Style, Function
from pyutter.widgets.layout import Padding


class FlatButton(ButtonWidget):
    def __init__(self, children: List[Any], id=None, style: Style = None, action: Function = None):
        style = style if style is not None else Style()
        style['border'] = '0'
        style['background'] = 'none'
        style['box-shadow'] = 'none'
        style['border-radius'] = '0px'

        super().__init__([Padding.all(pad=8, children=children)], id, style, action)


class RaisedButton(ButtonWidget):
    def __init__(self, children: List[Any], id=None, style: Style = None, action: Function = None):
        style = style if style is not None else Style()
        style['border'] = '0'
        style['box-shadow'] = 'none'
        style['border-radius'] = '0px'

        super().__init__([Padding.all(pad=8, children=children)], id, style, action)
