from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
	name='tailread',
	version='1.0.0',
	license='MIT',
	description='A Simple line generator from tail of file',
	long_description=long_description,
	long_description_content_type="text/markdown",
	author = 'HS Moon',
	author_email = 'pbr112@naver.com',
	py_modules = ['tailread'],
	install_requires=[],
	keywords=['tail', 'python tail', 'tailread'],
	url='https://github.com/zwolf21/tailread',
	packages=find_packages(exclude=['contrib', 'docs', 'test']),
	classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
	python_requires=">=3.4"
)