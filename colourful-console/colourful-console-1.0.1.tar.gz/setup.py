from setuptools import setup, find_packages

with open('README.md', encoding='utf8') as f:
    long_description = f.read()

setup(
    name='colourful-console',
    version='1.0.1',
    author='Sirshak Bohara',
    author_email='021neb459@sxc.edu.np',
    description='A simple python package to print colors in terminal using simple markup syntax',
    long_description=long_description,
    license='MIT',
    url='https://github.com/sirshakbohara/colourful-console',
    keywords=[
        'python color',
        'console color',
        'terminal colors',
        'markdown colors'
    ],
    package_dir={'': 'src'},
    packages=find_packages('src')
)