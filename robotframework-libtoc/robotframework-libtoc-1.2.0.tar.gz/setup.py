# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['robotframework_libtoc']

package_data = \
{'': ['*']}

install_requires = \
['robotframework>=4']

entry_points = \
{'console_scripts': ['libtoc = robotframework_libtoc.libtoc:main']}

setup_kwargs = {
    'name': 'robotframework-libtoc',
    'version': '1.2.0',
    'description': 'Docs and TOC generator for Robot Framework resources and libs',
    'long_description': "## Robot Framework LibTOC\n\n## What it does\nThis tool generates docs using Robot Framework [Libdoc](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#libdoc) for an entire folder with Robot Framework resources/libs and creates a TOC (Table of Content) file for them\n\n## Why use it\nThe Robot Framework Libdoc tool normally generates a HTML file for a single keyword library or a resource file.\nIf you have several keyword libraries, you just get several separate HTML files.\n\nThis tool collects separate keyword documentation files in one place and creates a TOC (Table of content) page\nwith links to these files.   \nThe result is a folder with several static HTML pages which can be placed somewhere \nin the intranet or uploaded as CI artifact - so everybody can easily access the keywords docs.\n\n### Here is the example screenshot\n![](Screenshot.png)\n\n## How it works\n- The tool goes through the specified folder with RF resources and it's **direct** subfolders\n- It looks for the **config files** named `.libtoc` which contain:\n    1. Paths to resource files in [glob format](https://en.wikipedia.org/wiki/Glob_(programming)) which you would like to create docs for\n    2. Installed RF libraries (names and necessary import params like described in [libdoc user guide](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#general-usage))\n        > Other libdoc CLI options (e.g. version or name of the output file) are not supported\n- Then it gererates the docs using `libdoc` - both for files paths, resolved from the glob patterns, and for the installed libraries. The created HTML files are places in the **libtoc output_dir** - keeping the original subfolder structure of resources\n- Finally it generates a **TOC (Table of Contents)** HTML page with links to all the generated HTML files.\n The navigation tree structure in the TOC repeats the folder tree structure.\n## Example of a `.libtoc` config file\n```\n[paths]\n# Use glob patterns\n**/*.robot\n**/*.resource\n**/*.py\n\n[libs]\n# Use RF library names with params - like for libdoc\nSeleniumLibrary\nRemote::http://10.0.0.42:8270\n# You can use environment variables in lib params\nSomeLib::$some_env_var/somepath\n```\n> The config file must contain at least one of the sections (`[paths]`, `[libs]` or both)\n## How to install it\n### System requirements\n- Python >=3.9\n- Robot Framework\n### Installation using pip\n```shell\npip install robotframework-libtoc\n```\n\n## How to use it\n- Create the `.libtoc` config files in subfolders where you need docs to be created.\n    > A config file directly in the root of the resources folder is valid, but not mandatory.\n- Run `libtoc`. The last `resources_dir` parameter is mandatory, others are optional:\n    - `-d, --output_dir`\n    - `--config_file`\n    - `--toc_file`\n    - `--toc_template`\n    - `--homepage_template`\n\n    Examples:\n    ```shell\n    libtoc example_resources\n    libtoc --output_dir docs example_resources\n    libtoc --output_dir docs --toc_file MY_SPECIAL_NAME_FOR_DOCS.html example_resources\n    libtoc --toc_template MY_CUSTOM_TOC.html --homepage_template MY_CUSTOM_HOMEPAGE.html example_resources\n    ```\n\n- Open the created file, e.g. `docs\\keyword_docs.html`\n\n## How to change the TOC and the homepage HTML templates\nThe default HTML template files are located in the python installation directory (usually something like `<python_dir>\\lib\\site-packages\\robotframework_libtoc`) and can be changed if necessary.   \nIt's also possible to provide custom HTML template files using the `--toc_template` and `--homepage_template` options.\n",
    'author': 'Andre Mochinin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/amochin/robotframework-libtoc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
