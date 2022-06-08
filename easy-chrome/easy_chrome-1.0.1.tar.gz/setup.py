import setuptools

setuptools.setup(
    name="easy_chrome",
    version="1.0.1",
    author="VanCuong",
    author_email="vuvancuong94@gmail.com",
    description="easy selenium chrome for window",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_packages(),
    install_requires=[
       'selenium',
       'requests'
    ],
    python_requires=">=3.7",
)
