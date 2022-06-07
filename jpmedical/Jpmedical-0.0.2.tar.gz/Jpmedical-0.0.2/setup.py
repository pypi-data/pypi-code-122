import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Jpmedical",
    version="0.0.2",
    author="naoto miyasaka",
    author_email="s2022064@stu.musashino-u.ac.jp",
    description='A package for visualization of total of Health expenditures, if people all over the world are Japnanese"',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/miyasaka007/Jpmedical-main",
    project_urls={
        "Bug Tracker": "https://github.com/miyasaka007/Jpmedical-main",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['Jpmedical'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'Jpmedical = Jpmedical:main'
        ]
    },
)
