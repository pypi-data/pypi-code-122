import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pyutter.core.primitive import View
from pyutter.widgets.layout import Center
from pyutter.widgets.text import H1

root = View([
    Center([H1(child=["Hello World"])])
])

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def demo():
    return root()


if __name__ == "__main__":
    uvicorn.run("hello_world:app", reload=True, host="127.0.0.1", port=5000, log_level="info")
