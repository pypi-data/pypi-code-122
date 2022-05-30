from setuptools import setup

with open("./README.md") as f:
    long_desc: str = f.read()

if __name__ == "__main__":
    setup(
        name="cereal-py",
        version="1.0",
        author="Joshua Auchincloss",
        author_email="<joshua.auchincloss@proton.me>",
        description="Create an iterable set of pointers to a specified length. Utilities for working with ZeroIntensity's pointers.py",
        long_description_content_type="text/markdown",
        long_description=long_desc,
        packages=["cereal"],
        keywords=["python", "cereal", "pointers"],
        install_requires=["typing_extensions", "pointers.py"],
        classifiers=[
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
        ],
        license="MIT",
        project_urls={
            "Source": "https://github.com/joshua-auchincloss/cereal",
            "Documentation": "https://cereal-py.netlify.app",
        },
        package_dir={"": "src"},
    )
