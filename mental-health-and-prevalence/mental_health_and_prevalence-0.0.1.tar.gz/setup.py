import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mental_health_and_prevalence",
    version="0.0.1",
    author="riko watanabe",
    author_email="s2022039@stu.musashino-u.ac.jp",
    description="Trends in the incidence of psychosis worldwide",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RikoWatanabe/MentalHelse.git",
    project_urls={
        "Bug Tracker": "https://github.com/RikoWatanabe/MentalHelse.git",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['mental_health_and_prevalence'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'mental_health_and_prevalence = mental_health_and_prevalence:main'
        ]
    },
)
