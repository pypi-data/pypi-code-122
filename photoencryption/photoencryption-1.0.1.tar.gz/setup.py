from setuptools import setup, find_packages

setup(
    name='photoencryption',
    packages=find_packages(),
    version='1.0.1',
    description='Encrypting and decrypting messages from images',
    author='Bruno Faliszewski',
    license='MIT',
    install_requires=['pillow', 'numpy'],
    project_urls={
        'homepage' : 'https://github.com/BrunoFaliszewski/PhotoEncryption'
    }
)