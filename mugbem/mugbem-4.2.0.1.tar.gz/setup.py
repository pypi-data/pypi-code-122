import setuptools


def setup():
    setuptools.setup(
        name="mugbem",
        version='4.2.0.1',
        author="JC",
        author_email="jeniokatutza@gmail.com",
        description="mugbem",
        long_description="mugbem",
        packages=setuptools.find_packages(),
        python_requires=">=3.8",
        install_requires=[
            'websocket-client',
            'requests',
            'rel'
        ],
        package_dir={
            'mugbem': 'mugbem'
        }
    )


if __name__ == "__main__":
    setup()
