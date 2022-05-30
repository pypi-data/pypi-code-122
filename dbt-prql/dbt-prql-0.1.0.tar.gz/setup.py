# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dbt_prql']

package_data = \
{'': ['*']}

install_requires = \
['dbt-core==1.1.0', 'pyprql>=0.5.0']

setup_kwargs = {
    'name': 'dbt-prql',
    'version': '0.1.0',
    'description': 'Write PRQL in dbt models',
    'long_description': "# dbt-prql\n\ndbt-prql allows writing PRQL in dbt models.\n\nTrivial Example:\n\n```elm\n{% prql %}\nfrom employees\nfilter (age | in 20..30)\n{% endprql %}\n```\n\n...compiles to:\n\n```sql\nSELECT\n  employees.*\nFROM\n  employees\nWHERE\n  age BETWEEN 20\n  AND 30\n```\n\nMore complex example:\n\n```elm\n{% prql %}\nfrom {{ source('salesforce', 'in_process') }}\nderive expected_sales = probability * value\njoin {{ ref('team', 'team_sales') }} [name]\ngroup name (\n    aggregate (expected_sales)\n)\n{% endprql %}\n```\n\n...compiles to:\n\n```sql\nSELECT\n  name,\n  {{ source('salesforce', 'in_process') }}.probability * {{ source('salesforce', 'in_process') }}.value AS expected_sales\nFROM\n  {{ source('salesforce', 'in_process') }}\n  JOIN {{ ref('team', 'team_sales') }} USING(name)\nGROUP BY\n  name\n```\n\n## Functionality\n\n- Any text between `{% prql %}` and `{% endprql %}` tags will be compiled from\n  PRQL to SQL.\n- Any text within the PRQL query that's surrounded by `{{...}}` will be passed\n  through to dbt parser without modification.\n\n## Installation\n\n```sh\npip install dbt-prql\n```\n\n## Current state\n\nCurrently this in an early state. But it's enthusiastically supported —\xa0if there\nare any problems, please open an issue.\n\nNote that we need to release a new `pyprql` version for this to pass jinja\nexpressions through, which we'll do in the next couple of days.\n\n## Is this magic?\n\nIt's much worse.\n\nUnfortunately, it's not possible to add behavior to dbt beyond the database\nadapters (e.g. `dbt-bigquery`) or jinja-only plugins (e.g. `dbt-utils`). So this\nlibrary hacks the python import system to monkeypatch dbt's jinja environment\nwith an additional jinja extension, which avoids the need for any changes to\ndbt.\n\nThanks to\n[mtkennerly/poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning)\nfor the technique.\n\nThis isn't stable between dbt versions, since it relies on internal dbt APIs.\nThe technique is also normatively bad —\xa0it runs a few lines of code every time\nthe python interpreter starts — whose errors could lead to very confusing bugs\nbeyond the domain of the problem (though in the case of this code, it's small\nand well-constructed™).\n\nIf there's ever any concern that the library might be causing a problem, just\nset an environment variable `DBT_PRQL_DISABLE=1`, and this library won't\nmonkeypatch anything. It's also fully uninstallable with `pip uninstall\ndbt-prql`.\n",
    'author': 'Maximilian Roos',
    'author_email': 'm@maxroos.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/prql/dbt-prql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
