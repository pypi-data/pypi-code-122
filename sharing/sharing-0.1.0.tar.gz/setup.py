"""
Packaging setup
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="sharing",
    version="0.1.0",
    author="Thibaut Guirimand",
    author_email="tguirimand@gmx.fr",
    description="Package allowing to share variables, configurations and counters between dependencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=required,
    url="https://gitlab.guirimand.eu/tguirimand/sharing",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development",
        "Environment :: Plugins"
    ],
    package_dir={
        'sharing': './sharing',
        },
    packages=[
        'sharing',
        ],
    package_data={},
    python_requires=">=3.8",
)
