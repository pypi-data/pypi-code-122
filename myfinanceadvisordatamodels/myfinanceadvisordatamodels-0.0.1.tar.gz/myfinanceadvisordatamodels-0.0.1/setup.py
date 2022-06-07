from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Data Models for My Finance Advisor'
LONG_DESCRIPTION = 'These are data models used with My Finance Advisor.'

# Setting up
setup(
        name="myfinanceadvisordatamodels", 
        version=VERSION,
        author="Richard Cerone",
        author_email="",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=['python', 'my-finance-advisor-lib'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)