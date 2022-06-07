import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dstoku.py",
    version="0.2.3",
    author="Hiroki Tonooka",
    author_email="s2022023@stu.musashino-u.ac.jp",
    description='A package for visualization of aggregate data of players in "dstoku.py"',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HirokiTonooka/DStokuronn",
    project_urls={
        "Bug Tracker": "https://github.com/HirokiTonooka/DStokuronn",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['test'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'test = test:main'
        ]
    },
)