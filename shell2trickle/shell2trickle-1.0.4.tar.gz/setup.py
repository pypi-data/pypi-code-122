from setuptools import setup


setup(
    name ='shell2trickle',
    version ='1.0.4',
    author ='Lania Kea',
    author_email ='lania.dang@visionwx.com',
    url ='',
    description ='use shell2trickle to post your new trickle!',
    long_description = 'Serve for Trickle, a better way to align your team!',
    long_description_content_type ="text/markdown",
    license ='MIT',
    packages = ["inbound", "trickle"],
    entry_points ={
        'console_scripts': [
            'trickle = inbound.main:main'
        ]
    },
    classifiers =(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords ='shell trickle',
    install_requires = [
        "requests"
    ],
    zip_safe = False
)