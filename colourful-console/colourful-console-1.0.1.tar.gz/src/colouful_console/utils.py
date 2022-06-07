import os
import sys

def title(string: str):
    """Sets the console title as per string

    Args:
        string (str): The string to make title
    """
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(message)
    
    else:
        sys.stdout.write(f'\x1b]2;{string}\x07')

def set_title(sep=' | ', **kwargs) -> None:
    """Sets the console title as keyword parameters

    Args:
        sep (str): The seperator to seperate arguments. Defaults to ' | '
        **kwargs: keyword arguments
    
    Example:
        >>> set_title(lang='python', version=3, foo='bar')

    \# this will set the title to 
    lang: python | version: 3 | foo: bar
    """
    message = []
    for key, value in kwargs.items():
        message.append(f'{key}: {value}')

    message = sep.join(message)
    title(message)


def clear() -> None:
    """
    Clears the command line
    Applicable for both win32 and unix/mac
    """
    os.system('cls') if os.name == 'nt' else os.system('clear')