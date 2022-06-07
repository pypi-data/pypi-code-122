import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pyutter.core.primitive import Style, Image, View
from pyutter.widgets.layout import Center, Row, Expanded, Padding, Spacer, Grid
from pyutter.widgets.material import Card, Chip
from pyutter.widgets.text import H2, P, H1

intro_string = '''The content on this page is generated from python code. Lorem ipsum dolor sit amet, consectetur  
adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,  
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in  
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non  
proident, sunt in culpa qui officia deserunt mollit anim id est laborum. '''

button_style = Style(width='50px')
image_style = Style(width='100%')
spacer = Spacer(width=10)
card_style = Style(width='400px')


def card_generator():
    for x in range(10):
        yield Card(children=[
            Image(src=f'https://picsum.photos/400/200?random={x}', style=image_style),
            Padding.all(pad=16,
                        children=[
                            H2(['Simple Card Object']),
                            Row(children=[
                                Expanded(),
                                Chip(children=[P(['Hello: ']), P(['👋'])]),
                            ]),
                            P([intro_string])
                        ])
        ], style=card_style
        )


root = View([
    Center(children=[
        Grid(children=[x for x in card_generator()]),
    ])
])

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def demo():
    return root.__properties__()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
