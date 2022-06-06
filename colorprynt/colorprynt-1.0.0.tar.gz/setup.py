from setuptools import setup

with open('README.md', 'r') as reader:
    long_description = reader.read()


setup(
    author='Jaedson Silva',
    author_email='imunknowuser@protonmail.com',
    name='colorprynt',
    version='1.0.0',
    description='Print color text easily.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['colorprynt'],
    license='MIT',
    project_urls={
        'Source code': 'https://github.com/jaedsonpys/colorprynt'
    }
)