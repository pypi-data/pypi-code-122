from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='helloworld-package-2022', 
    version='0.0.2', 
    description='Say hello!', 
    py_modules=["helloworld"],
    package_dir={'':'src'},
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
    "blessings ~= 1.7",
    ],
    extras_require = {
        "dev": [
            "pytest>=3.7",
            "tox",
            "mkdocs==1.1.2",  # static site generator for documentation in Markdown
            "mkdocs-material==7.1.5",  # Material support for MkDocs
            "mkdocs-minify-plugin==0.4.0",  # strips whitespaces in HTML markdown documentation pages
            "mkdocs-git-revision-date-localized-plugin==0.9.2",  # displays the date of the last git modification of a markdown page
            "mkdocs-git-authors-plugin==0.3.3",  # displays git authors of a markdown page
            "mkdocs-table-reader-plugin==0.5",  # enables automatic CSV imports as a table into a markdown page
            "mkdocs-img2fig-plugin==0.9.3",  # converts markdown encoded images to HTML figures
            "mknotebooks==0.7.0",  # enables inclusion of Jupyter notebook in markdown page
            "mkdocs-awesome-pages-plugin==2.5.0",  # enables naive configuration of page titles and their order
            "mkdocs-enumerate-headings-plugin==0.4.4",  # enumerates headings across markdown pages
            "mkdocs-print-site-plugin==1.2.3",  # allows visiters to File > Print > Save as PDF entire markdown documentation
            "mkgendocs==0.8.1"  # generate MkDocs pages from Google-style docstrings of Python functions
        ],
    },
    author="zack588",
    author_email="zakaribarj@yahoo.fr",
)
