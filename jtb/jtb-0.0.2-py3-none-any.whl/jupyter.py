from IPython.display import HTML, display

from IPython.utils import openpy
from pathlib import Path
import inspect

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def getCode(url=None, imp=None, file=None):
    if imp is not None:
        py = inspect.getsource(imp)
    elif url is not None:
        py = openpy.read_py_url(url)
    elif file is not None:
        py = openpy.read_py_file(str(file))
    else:
        raise Exception("Nothing given")
        
    display(HTML(highlight(py, PythonLexer(), HtmlFormatter())))
