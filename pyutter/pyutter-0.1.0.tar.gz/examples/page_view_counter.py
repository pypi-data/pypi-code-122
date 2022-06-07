import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pyutter.core.primitive import View
from pyutter.widgets.layout import Center, Row
from pyutter.widgets.text import H1

view_count = 0


def get_view_count():
    global view_count
    return H1(["View count: ", str(view_count)])


root = View([
    Center([Row([
        get_view_count])
    ])
]
)

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def demo():
    global view_count
    view_count += 1
    return root()


if __name__ == "__main__":
    uvicorn.run("page_view_counter:app", reload=True, host="0.0.0.0", port=5000, log_level="info")
