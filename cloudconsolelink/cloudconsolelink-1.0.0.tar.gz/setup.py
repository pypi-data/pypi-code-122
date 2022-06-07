import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# version of the module
__version__ = '1.0.0'


setuptools.setup(
    # Here is the module name.
    name="cloudconsolelink",

    # version of the module
    version=__version__,

    # Name of Maintainer
    maintainer="Cloudanix",

    # Maintainer Email address
    maintainer_email="purusottam@cloudanix.com",

    # Small Description about module
    description="Generate console links for cloud resources",

    long_description=long_description,

    # Specifying that we are using markdown file for description
    long_description_content_type="text/markdown",

    # Any link to reach this module, if you have any webpage or github profile
    url="https://github.com/Cloudanix/cloud-console-links",
    packages=setuptools.find_packages(),

    # classifiers like program is suitable for python3, just leave as it is.
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
