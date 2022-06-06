BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
CLOSE = '\033[m'

import sys
from typing import TextIO


def print(
    *values: str, 
    end: str = '\n',
    sep: str = '',
    file: TextIO = sys.stdout,
    color: str = 'white'
) -> None:
    if color == 'black':
        file.write(BLACK)
    elif color == 'red':
        file.write(RED)
    elif color == 'green':
        file.write(GREEN)
    elif color == 'yellow':
        file.write(YELLOW)
    elif color == 'blue':
        file.write(BLUE)
    elif color == 'purple':
        file.write(PURPLE)
    elif color == 'cyan':
        file.write(CYAN)
    elif color == 'white':
        file.write(WHITE)

    len_values = len(values)

    for i, v in enumerate(values):
        if type(v) not in (str, float, int):
            v = v.__repr__()

        file.write(v)
        if i != len_values - 1:
            file.write(sep)

    file.write(CLOSE)
    file.write(end)
