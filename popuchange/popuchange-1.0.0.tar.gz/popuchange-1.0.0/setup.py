import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="popuchange",
    version="1.0.0",
    author="takuma iwasaki",
    author_email="taku_2198@yahoo.co.jp",
    description='A package for visualization of population in japan"',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kuma2198/popuchange",
    project_urls={
        "Bug Tracker": "https://github.com/kuma2198/popuchange",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['popuchange'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'popuchange = popuchange:main'
        ]
    },
)
