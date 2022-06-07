#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='DataframePacking',
    version='22.06.07',
    #packages=['things_labels', 'things_labels.data', 'things_labels.data_labelling'],
    packages = find_packages(exclude=["*_old*", "*old_", "tests*", "venv*"]),
    license='',
    long_description=open('README.md').read(),
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        #"": ["*.csv", "*.tsv"],
    },
    # entry_points={
    #     "console_scripts": [
    #         "label_ages = things_labels.data_labelling.label_ages:main",
    #         "label_animism = things_labels.data_labelling.label_animism:main",
    #         "label_object_names_in_triplet = things_labels.data_labelling.label_object_names_in_triplet:main"
    #     ]
    # },
    install_requires=[
        "pandas>=0.24.1"
    ],
)



