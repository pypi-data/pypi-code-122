from setuptools import setup, find_packages


VERSION = '0.0.6'
DESCRIPTION = 'Fetch credentials of aks using azure-cli'

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
    name='az_creds',
    version=VERSION,
    license='GNU',
    author='Jilani Sayyad',
    author_email='sayyedjilani88@gmail.com',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/jilanisayyad/fetch_credentials',
    keywords=['get_creds', 'fetch_credentials', 'azure', 'aks', 'azure-cli'],
    install_requires=[
        'simple-term-menu',
        'pyyaml'
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'az_creds=fetch_app.credentials:main'
        ]
    }
)
