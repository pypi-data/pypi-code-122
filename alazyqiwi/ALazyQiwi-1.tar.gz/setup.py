from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='ALazyQiwi',
      version='1',
      description='Simple async library for qiwi farms',
      packages=['ALazyQiwi'],
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown',
      python_requires=">=3.10",
      py_modules=['httpx'],
)
