from pathlib import Path

import toml

with open(Path(__file__).parent.parent / "pyproject.toml") as f:
    data = f.read()

__version__ = toml.loads(data)["tool"]["poetry"]["version"]
