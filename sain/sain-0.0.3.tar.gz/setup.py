# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sain']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sain',
    'version': '0.0.3',
    'description': 'Standard Rust core types implementations for Python.',
    'long_description': '# sain\nA pure Python package that implements standard Rust core types for Python.\n\n\n## Install\nYou\'ll need Python 3.8 or higher.\n\nPyPI\n```rs\n$ pip install sain\n```\n\n## Examples\nMore stuff in [examples](https://github.com/nxtlo/sain/tree/master/examples)\n\n### `cfg`, `cfg_attr`\nConditionally include code.\n\n```py\nfrom sain import cfg, cfg_attr\n\n@cfg_attr(target_os="unix")\n# Calling this on a non-unix system will raise a RuntimeError\n# and the function will not run.\ndef run_when_unix() -> None:\n    import uvloop\n    uvloop.install()\n\nif cfg(target_arch="arm64"):\n    run_when_unix()\n\n# If this returns True, Function will be in scope.\nif cfg(requires_modules="hikari-tanjun"):\n    def create_client() -> tanjun.Client:\n        return tanjun.Client(...)\n\n# Assuming tanjun is not installed.\n# Calling the function will raise `NameError`\n# since its not in scope.\ncreate_client()\n```\n\n### `Option<T>` and `Some<T>`\nImplements the standard `Option` and `Some` types. An object that may be `None` or `T`.\n\n```py\nimport sain\nimport os\n\n# Stright up replace typing.Optional[str]\ndef get_token(key: str) -> sain.Option[str]:\n    # What os.getenv returns may be str or None.\n    return sain.Some(os.getenv(key))\n\n# Raises RuntimeError("No token found.") if os.getenv return None.\ntoken = get_token().expect("No token found.")\n\n# The classic way to handle this in Python would be.\nif token is None:\n    token = "..."\nelse:\n    ...\n\n# Replace this with `unwrap_or`.\n# Returning DEFAULT_TOKEN if it was None.\nenv_or_default = get_token().unwrap_or("DEFAULT_TOKEN")\n\n# Safe type hint is fine.\nas_none: sain.Option[str] = sain.Some(None)\nas_none.uwnrap_or(123)  # Error: Must be type `str`!\nassert as_none.is_none()\n```\n\n### Defaults\nA protocol that types can implement which have a default value.\n\n```py\nimport sain\nimport requests\n\nclass Session(sain.Default[requests.Session]):\n    # One staticmethod must be implemented and must return the same type.\n    @staticmethod\n    def default() -> requests.Session:\n        return requests.Session()\n\nsession = Session.default()\n```\n\n### Iter\nTurns normal iterables into `Iter` type.\n\n```py\nimport sain\n\nf = sain.Iter([1,2,3])\n# or f = sain.into_iter([1,2,3])\nassert 1 in f\n\nfor item in f.take_while(lambda i: i > 1):\n    print(item)\n```\n\n### Why\nThis is whats Python missing.\n\n### Notes\nSince Rust is a compiled language, Whatever predict in `cfg` and `cfg_attr` returns False will not compile.\n\nBut there\'s no such thing as this in Python, So `RuntimeError` will be raised and whatever was predicated will not run.\n',
    'author': 'nxtlo',
    'author_email': 'dhmony-99@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nxtlo/sain',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
