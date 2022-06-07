import setuptools
from qa_medindex_libs.version_package import get_version
DESCRIPTION = "A package for internal usage in The Medindex ru for pdf image compare"


setuptools.setup(
    name="medindex_firefighters_compare_pdf",
    #version=get_version(version="1.56"),
    version="1.56",
    author='kurzeneva.o',
    author_email='kurzeneva.o@medindex.ru',
    description=DESCRIPTION,
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)
