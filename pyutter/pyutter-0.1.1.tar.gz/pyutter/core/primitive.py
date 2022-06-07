import inspect
import string
from random import choice
from typing import List, Any

from pyutter.core_routing import state_router, file


def generate_id():
    return ''.join([choice(string.ascii_letters) for n in range(6)])


class Style(dict):
    def __init__(self, id=None, *args, **kwargs):
        super().__init__()
        self.update(*args, **kwargs)
        self.id = id if id is not None else generate_id()


class Function(dict):
    def __init__(self, func, method="POST", event='click', *args, **kwargs):
        super().__init__()
        self.callable = func
        self.update(*args, **kwargs)
        self.id = generate_id()
        self.event = event
        self.method = method

        @state_router.api_route('/' + self.id, methods=[method])
        def _(q: dict):
            return func(**q)

        self.traits = {
            "actionId": self.id,
            "actionVars": list(self.keys()),
            "children": self,
            "method": self.method,
        }

    def __properties__(self):
        return {
            "actionId": self.id,
            "actionVars": list(self.keys()),
            'children': self,
            "traits": self.traits
        }

    def __call__(self, *args, **kwargs):
        return self.__properties__()


# TODO: we also need a local state
class State(dict):
    def __init__(self, name=generate_id(), value=None):
        super().__init__()
        self.name = name
        self.value = value
        self.id = generate_id()
        self.update({self.id: {self.name: self.value}})

        self.traits = {
            "actionId": self.id,
            self.name: self.value,
            "place": "innerHTML"
        }

    def __repr__(self):
        return str(self.value)

    def __properties__(self):
        return self.traits


class TextController(State):
    def __init__(self, name=generate_id(), value=None):
        super().__init__()


class Widget:
    def __init__(self, tag, children: List[Any] = None, id=None, style=None, action=None):
        self.traits = {
            'render': 1
        }
        self.tag = tag
        self.child = children if children is not None else []
        self.id = id if id is not None else generate_id()
        self.style = style if style is not None else Style()
        # self.style['display'] = 'flex'

        self.action = action

    def __style__(self):
        style = [self.style]
        for x in self.child:
            if inspect.isfunction(x):
                t_acc, t_style = x().__style__()
            else:
                t_acc, t_style = x.__style__()
            style.extend(t_style)

        return '', style

    def __properties__(self):
        return {
            'id': self.id,
            'class': self.style.id,
            'style': self.style,
            'tag': self.tag,
            'children': [x()() if inspect.isfunction(x) else x() for x in self.child],
            'traits': self.traits,
        }

    def __repr__(self):
        return self.__style__()

    def __call__(self, *args, **kwargs):
        return self.__properties__()


class View(Widget):
    def __init__(self, children):
        style = Style()
        style['background-color'] = "#dfe5e8"
        super().__init__('body', children, style=style)

    def __properties__(self):
        style = ''
        style_list = [self.style]

        for x in self.child:
            if inspect.isfunction(x):
                t_acc, t_style = x().__style__()
            else:
                t_acc, t_style = x.__style__()
                style_list.extend(t_style)

        styles = {x.id: x for x in style_list}
        for x in styles.values():
            style += f'.{x.id}' + '{' + ''.join(f"{k}:{v};" for k, v in x.items()) + '}'

        desc = {
            'id': self.id,
            'class': self.style.id,
            'style': self.style,
            'tag': self.tag,
            'traits': self.traits,
            'children': [x()() if inspect.isfunction(x) else x() for x in self.child]
        }
        return f'''<!DOCTYPE html>
<html>
    <head>
<meta name="viewport" content="width=device-width, initial-scale=0.86, maximum-scale=5.0, minimum-scale=0.86">
<title>The View</title>
        <style>
html, body, div {{ margin:0;}}
{style}
</style>
    </head>
    <body>
        <script>
var body = {desc};
{file()}
window.onload = render(body, null);
window.post = function(url, data) {{
    return fetch(url, {{
        method: "POST",
        body: JSON.stringify(data)
    }});
}};
        </script>
    </body>
</html>'''


class Text(Widget):
    def __init__(self, tag='plain', text: str = '', id=None, style: Style = None):
        super().__init__(tag, [], id, style)
        self.traits['text'] = text

        if type(text) is not str:
            self.traits['sourceId'] = text.id


class TextWidget(Widget):
    def __init__(self, tag='div', child: List[Any] = None, id=None, style: Style = None):
        child = [] if child is None else child
        objs = []
        for obj in child:
            if not issubclass(obj.__class__, Widget) or not issubclass(obj.__class__, State):
                t = Text(text=obj)
                objs.append(t)
            else:
                objs.append(obj)
        super().__init__(tag, objs, id, style)


class ButtonWidget(Widget):
    def __init__(self, children: List[Any], id=None, style: Style = None, action: Function = None):
        super().__init__('button', children, id, style, action)

        if self.action is not None:
            self.traits['actionId'] = action.id
            self.traits['actionVars'] = action()
            self.traits['actionEvent'] = action.event


class Image(Widget):
    def __init__(self, src, id=None, style: Style = None):
        super().__init__('img', [], id, style)
        self.traits['src'] = src


class Video(Widget):
    def __init__(self, src, id=None, style: Style = None):
        super().__init__('video', [], id, style)
        self.traits['src'] = src


class Input(Widget):
    def __init__(self, type, children: List[Any], id=None, style: Style = None):
        super().__init__('input', children, id, style)
        self.traits['input'] = type
