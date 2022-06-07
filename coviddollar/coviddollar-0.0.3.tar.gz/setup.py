import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coviddollar",
    version="0.0.3",
    author="ami takenaka",
    author_email="amiami0806takenaka@gmail.com",
    description="A package for comparison dollar exchange rate fluctuations and changes in the number of new covid-19 infections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amitake/coviddollar",
    project_urls={
        "Bug Tracker": "https://github.com/amitake/coviddollar",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['coviddollar'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'coviddollar = coviddollar:main'
        ]
    },
)
