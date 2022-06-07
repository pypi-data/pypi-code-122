import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="timeofsleep", # 設定する名前
    version="0.0.1", # バージョン設定
    author="kyohei fujimori.kyohei@gmail.com", # 名前
    author_email="", # メアド変更
    description='It is a package that visualizes sleep time and sleep quality.', # 説明文書書き換え
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kyohei-2022029/timeofsleep/tree/master", # GitHubURL
    project_urls={
        "Bug Tracker": "https://github.com/kyohei-2022029/timeofsleep/tree/master", #GitHubURL
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['timeofsleep'], # 設定するモジュール名
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'timeofsleep = timeofsleep:main' # srcの中にある.pyの手前の文字
        ]
    },
)