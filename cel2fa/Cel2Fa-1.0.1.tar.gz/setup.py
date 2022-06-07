import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Cel2Fa",
    version="1.0.1",
    author="Hyuga Taki",
    author_email="",
    description="Read Celsius csv file and change to Fahrenheit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HTuniv/CelsiusToFahrenheit",
    project_urls={
        "Bug Tracker": "https://github.com/HTuniv/CelsiusToFahrenheit",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['Cel2Fa'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'Cel2Fa = Cel2Fa:main'
        ]
    },
)
