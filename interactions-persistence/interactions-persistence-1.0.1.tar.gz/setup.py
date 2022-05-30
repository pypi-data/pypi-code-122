from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="interactions-persistence",
    version="1.0.1",
    description="Encode objects in custom_ids.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dworv/interactions-persistence",
    author="Dworv",
    author_email="dwarvyt@gmail.com",
    license="GNU",
    packages=["interactions.ext.persistence"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["discord-py-interactions"],
)