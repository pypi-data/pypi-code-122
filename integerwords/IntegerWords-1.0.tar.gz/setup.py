import setuptools


with open("README.md", "r") as fh:
	long_desc = fh.read()


setuptools.setup(name='IntegerWords',
      version='1.0',
      description='A python3 module that converts numbers to English words.  For example "5" -> "five"',
      long_description = long_desc,
      long_description_content_type="text/markdown",
      url='https://github.com/deadmund/IntegerWords',
      author='Ed Novak',
      author_email="enovak@fandm.edu",
      license='GPL-v3',
      py_modules=['IntegerWords'],
      entry_points={'console_scripts':['IntegerWords = IntegerWords.__main__:main']},
      package_dir={"": "src"},
      packages=setuptools.find_packages(where="src"),
      python_requires=">=3.0",
      classifiers=["Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"])
