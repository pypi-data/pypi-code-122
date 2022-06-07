import setuptools
from circe_ui import version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="circe-ui-CERTIC",
    version=version,
    author="Mickaël Desfrênes",
    author_email="mickael.desfrenes@unicaen.fr",
    description="Circe UI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.unicaen.fr/fnso/i-fair-ir/circe-server",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "circe-client-CERTIC",
        "argh",
        "sanic",
        "itsdangerous",
        "aiofiles",
        "python-dotenv",
    ],
    python_requires=">=3.9",
    include_package_data=True,
    entry_points={
        "console_scripts": ["circeui=circe_ui.__main__:run_cli"],
    },
)
