import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tokyopopuchange",
    version="1.0.0",
    author="takuma iwasaki",
    author_email="s2022005@stu.musashino-u.ac.jpp",
    description='A package for visualization of population in tokyo"',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kuma2198/tokyopopuchange",
    project_urls={
        "Bug Tracker": "https://github.com/kuma2198/tokyopopuchange",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['tokyopopuchange'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'tokyopopuchange = tokyopopuchange:main'
        ]
    },
)
