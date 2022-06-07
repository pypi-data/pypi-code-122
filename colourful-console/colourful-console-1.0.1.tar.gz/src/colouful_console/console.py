import os
from .constants import (
    PATTERNS, 
    TAGS, 
    RESET
)

def init():
    """initalizes the packages and the color codes for win32

    Returns:
        int: 1 for success
    """
    # In win32 this magically enables the cmd & poweshell to print ANSI color codes
    os.system('')
    return 1

def write_line(string: str, end='\n'):
    """Prints the `string` with markup colors

    Args:
        string (str): The string with markup tags
        end (str, optional): The character to be printed at the end. Defaults to '\\n'.

    Returns:
        int: 1 for success
    """
    for pattern, color in PATTERNS.items():
        matches = pattern.findall(string)
        
        for match in matches:
            string = string.replace(match, f'{color}{match}{RESET}')

    for tag in TAGS:
        string = string.replace(tag, '')

    print(string, end=end)
    return 1 # return 1 for test purposes

def read_line(string: str, end=''):
    """Prints the `string` with markup colors and takes user input

    Args:
        string (str): The string with markup tags
        end (str, optional): The character to be printed at the end. Defaults to ''.

    Returns:
        int: the user input
    """
    write_line(string, end)
    return input()