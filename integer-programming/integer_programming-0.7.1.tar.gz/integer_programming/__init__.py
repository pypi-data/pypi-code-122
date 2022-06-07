import pathlib

HERE = pathlib.Path(__file__).parent
__version__ = (HERE / "VERSION").read_text().strip()

class integer_programming:
    
    from integer_programming.steinitz import steinitz_ip as steinitz_ip