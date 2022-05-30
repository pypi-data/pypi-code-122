import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-lambda-layer-wget",
    "version": "2.0.95",
    "description": "Lambda Layer for wget",
    "license": "Apache-2.0",
    "url": "https://github.com/clarencetw/cdk-lambda-layer-wget.git",
    "long_description_content_type": "text/markdown",
    "author": "clarencetw<mr.lin.clarence@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/clarencetw/cdk-lambda-layer-wget.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_lambda_layer_wget",
        "cdk_lambda_layer_wget._jsii"
    ],
    "package_data": {
        "cdk_lambda_layer_wget._jsii": [
            "cdk-lambda-layer-wget@2.0.95.jsii.tgz"
        ],
        "cdk_lambda_layer_wget": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.59.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
