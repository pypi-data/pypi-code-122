# -*- coding: utf-8 -*-
 
"""
Author     : CG
Description: 
"""
 
import setuptools
 
 
with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
 
 
setuptools.setup(
    name='opencg',  # 模块名称
    version="0.1",  # 当前版本
    author="CG",  # 作者
    author_email="",  # 作者邮箱
    description="函数计时器",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    # url="",  # 模块github地址
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    # install_requires=[],
    python_requires='>=3.6',
)
