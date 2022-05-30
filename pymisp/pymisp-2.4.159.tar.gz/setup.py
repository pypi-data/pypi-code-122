# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymisp',
 'pymisp.data.misp-objects',
 'pymisp.data.misp-objects.tools',
 'pymisp.tools']

package_data = \
{'': ['*'],
 'pymisp': ['data/*'],
 'pymisp.data.misp-objects': ['.github/workflows/*',
                              'docs/*',
                              'objects/ail-leak/*',
                              'objects/ais-info/*',
                              'objects/android-app/*',
                              'objects/android-permission/*',
                              'objects/annotation/*',
                              'objects/anonymisation/*',
                              'objects/apivoid-email-verification/*',
                              'objects/artifact/*',
                              'objects/asn/*',
                              'objects/attack-pattern/*',
                              'objects/authentication-failure-report/*',
                              'objects/authenticode-signerinfo/*',
                              'objects/av-signature/*',
                              'objects/bank-account/*',
                              'objects/bgp-hijack/*',
                              'objects/bgp-ranking/*',
                              'objects/blog/*',
                              'objects/boleto/*',
                              'objects/btc-transaction/*',
                              'objects/btc-wallet/*',
                              'objects/cap-alert/*',
                              'objects/cap-info/*',
                              'objects/cap-resource/*',
                              'objects/cloth/*',
                              'objects/coin-address/*',
                              'objects/command-line/*',
                              'objects/command/*',
                              'objects/concordia-mtmf-intrusion-set/*',
                              'objects/cookie/*',
                              'objects/cortex-taxonomy/*',
                              'objects/cortex/*',
                              'objects/course-of-action/*',
                              'objects/covid19-csse-daily-report/*',
                              'objects/covid19-dxy-live-city/*',
                              'objects/covid19-dxy-live-province/*',
                              'objects/cowrie/*',
                              'objects/cpe-asset/*',
                              'objects/credential/*',
                              'objects/credit-card/*',
                              'objects/crypto-material/*',
                              'objects/cytomic-orion-file/*',
                              'objects/cytomic-orion-machine/*',
                              'objects/dark-pattern-item/*',
                              'objects/ddos/*',
                              'objects/device/*',
                              'objects/diameter-attack/*',
                              'objects/dkim/*',
                              'objects/dns-record/*',
                              'objects/domain-crawled/*',
                              'objects/domain-ip/*',
                              'objects/edr-report/*',
                              'objects/elf-section/*',
                              'objects/elf/*',
                              'objects/email/*',
                              'objects/employee/*',
                              'objects/error-message/*',
                              'objects/exploit-poc/*',
                              'objects/facebook-account/*',
                              'objects/facebook-group/*',
                              'objects/facebook-page/*',
                              'objects/facebook-post/*',
                              'objects/facial-composite/*',
                              'objects/fail2ban/*',
                              'objects/favicon/*',
                              'objects/file/*',
                              'objects/forensic-case/*',
                              'objects/forensic-evidence/*',
                              'objects/forged-document/*',
                              'objects/ftm-Airplane/*',
                              'objects/ftm-Assessment/*',
                              'objects/ftm-Asset/*',
                              'objects/ftm-Associate/*',
                              'objects/ftm-Audio/*',
                              'objects/ftm-BankAccount/*',
                              'objects/ftm-Call/*',
                              'objects/ftm-Company/*',
                              'objects/ftm-Contract/*',
                              'objects/ftm-ContractAward/*',
                              'objects/ftm-CourtCase/*',
                              'objects/ftm-CourtCaseParty/*',
                              'objects/ftm-Debt/*',
                              'objects/ftm-Directorship/*',
                              'objects/ftm-Document/*',
                              'objects/ftm-Documentation/*',
                              'objects/ftm-EconomicActivity/*',
                              'objects/ftm-Email/*',
                              'objects/ftm-Event/*',
                              'objects/ftm-Family/*',
                              'objects/ftm-Folder/*',
                              'objects/ftm-HyperText/*',
                              'objects/ftm-Image/*',
                              'objects/ftm-Land/*',
                              'objects/ftm-LegalEntity/*',
                              'objects/ftm-License/*',
                              'objects/ftm-Membership/*',
                              'objects/ftm-Message/*',
                              'objects/ftm-Organization/*',
                              'objects/ftm-Ownership/*',
                              'objects/ftm-Package/*',
                              'objects/ftm-Page/*',
                              'objects/ftm-Pages/*',
                              'objects/ftm-Passport/*',
                              'objects/ftm-Payment/*',
                              'objects/ftm-Person/*',
                              'objects/ftm-PlainText/*',
                              'objects/ftm-PublicBody/*',
                              'objects/ftm-RealEstate/*',
                              'objects/ftm-Representation/*',
                              'objects/ftm-Row/*',
                              'objects/ftm-Sanction/*',
                              'objects/ftm-Succession/*',
                              'objects/ftm-Table/*',
                              'objects/ftm-TaxRoll/*',
                              'objects/ftm-UnknownLink/*',
                              'objects/ftm-UserAccount/*',
                              'objects/ftm-Vehicle/*',
                              'objects/ftm-Vessel/*',
                              'objects/ftm-Video/*',
                              'objects/ftm-Workbook/*',
                              'objects/game-cheat/*',
                              'objects/geolocation/*',
                              'objects/git-vuln-finder/*',
                              'objects/github-user/*',
                              'objects/gitlab-user/*',
                              'objects/gtp-attack/*',
                              'objects/hashlookup/*',
                              'objects/http-request/*',
                              'objects/identity/*',
                              'objects/ilr-impact/*',
                              'objects/ilr-notification-incident/*',
                              'objects/image/*',
                              'objects/impersonation/*',
                              'objects/imsi-catcher/*',
                              'objects/infrastructure/*',
                              'objects/instant-message-group/*',
                              'objects/instant-message/*',
                              'objects/intel471-vulnerability-intelligence/*',
                              'objects/intelmq_event/*',
                              'objects/intelmq_report/*',
                              'objects/internal-reference/*',
                              'objects/interpol-notice/*',
                              'objects/iot-device/*',
                              'objects/iot-firmware/*',
                              'objects/ip-api-address/*',
                              'objects/ip-port/*',
                              'objects/irc/*',
                              'objects/ja3/*',
                              'objects/ja3s/*',
                              'objects/jarm/*',
                              'objects/keybase-account/*',
                              'objects/language-content/*',
                              'objects/leaked-document/*',
                              'objects/legal-entity/*',
                              'objects/lnk/*',
                              'objects/macho-section/*',
                              'objects/macho/*',
                              'objects/mactime-timeline-analysis/*',
                              'objects/malware-config/*',
                              'objects/meme-image/*',
                              'objects/microblog/*',
                              'objects/mutex/*',
                              'objects/narrative/*',
                              'objects/netflow/*',
                              'objects/network-connection/*',
                              'objects/network-profile/*',
                              'objects/network-socket/*',
                              'objects/news-agency/*',
                              'objects/news-media/*',
                              'objects/open-data-security/*',
                              'objects/organization/*',
                              'objects/original-imported-file/*',
                              'objects/paloalto-threat-event/*',
                              'objects/parler-account/*',
                              'objects/parler-comment/*',
                              'objects/parler-post/*',
                              'objects/passive-dns-dnsdbflex/*',
                              'objects/passive-dns/*',
                              'objects/passive-ssh/*',
                              'objects/paste/*',
                              'objects/pcap-metadata/*',
                              'objects/pe-section/*',
                              'objects/pe/*',
                              'objects/person/*',
                              'objects/personification/*',
                              'objects/pgp-meta/*',
                              'objects/phishing-kit/*',
                              'objects/phishing/*',
                              'objects/phone/*',
                              'objects/postal-address/*',
                              'objects/probabilistic-data-structure/*',
                              'objects/process/*',
                              'objects/publication/*',
                              'objects/python-etvx-event-log/*',
                              'objects/r2graphity/*',
                              'objects/ransom-negotiation/*',
                              'objects/reddit-account/*',
                              'objects/reddit-comment/*',
                              'objects/reddit-post/*',
                              'objects/reddit-subreddit/*',
                              'objects/regexp/*',
                              'objects/registry-key/*',
                              'objects/regripper-NTUser/*',
                              'objects/regripper-sam-hive-single-user/*',
                              'objects/regripper-sam-hive-user-group/*',
                              'objects/regripper-software-hive-BHO/*',
                              'objects/regripper-software-hive-appInit-DLLS/*',
                              'objects/regripper-software-hive-application-paths/*',
                              'objects/regripper-software-hive-applications-installed/*',
                              'objects/regripper-software-hive-command-shell/*',
                              'objects/regripper-software-hive-software-run/*',
                              'objects/regripper-software-hive-userprofile-winlogon/*',
                              'objects/regripper-software-hive-windows-general-info/*',
                              'objects/regripper-system-hive-firewall-configuration/*',
                              'objects/regripper-system-hive-general-configuration/*',
                              'objects/regripper-system-hive-network-information/*',
                              'objects/regripper-system-hive-services-drivers/*',
                              'objects/report/*',
                              'objects/research-scanner/*',
                              'objects/rogue-dns/*',
                              'objects/rtir/*',
                              'objects/sandbox-report/*',
                              'objects/sb-signature/*',
                              'objects/scheduled-event/*',
                              'objects/scrippsco2-c13-daily/*',
                              'objects/scrippsco2-c13-monthly/*',
                              'objects/scrippsco2-co2-daily/*',
                              'objects/scrippsco2-co2-monthly/*',
                              'objects/scrippsco2-o18-daily/*',
                              'objects/scrippsco2-o18-monthly/*',
                              'objects/script/*',
                              'objects/security-playbook/*',
                              'objects/shell-commands/*',
                              'objects/shodan-report/*',
                              'objects/short-message-service/*',
                              'objects/shortened-link/*',
                              'objects/social-media-group/*',
                              'objects/software/*',
                              'objects/spearphishing-attachment/*',
                              'objects/spearphishing-link/*',
                              'objects/splunk/*',
                              'objects/ss7-attack/*',
                              'objects/ssh-authorized-keys/*',
                              'objects/stix2-pattern/*',
                              'objects/submarine/*',
                              'objects/suricata/*',
                              'objects/target-system/*',
                              'objects/tattoo/*',
                              'objects/telegram-account/*',
                              'objects/temporal-event/*',
                              'objects/threatgrid-report/*',
                              'objects/timecode/*',
                              'objects/timesketch-timeline/*',
                              'objects/timesketch_message/*',
                              'objects/timestamp/*',
                              'objects/tor-hiddenservice/*',
                              'objects/tor-node/*',
                              'objects/tracking-id/*',
                              'objects/transaction/*',
                              'objects/translation/*',
                              'objects/trustar_report/*',
                              'objects/tsk-chats/*',
                              'objects/tsk-web-bookmark/*',
                              'objects/tsk-web-cookie/*',
                              'objects/tsk-web-downloads/*',
                              'objects/tsk-web-history/*',
                              'objects/tsk-web-search-query/*',
                              'objects/twitter-account/*',
                              'objects/twitter-list/*',
                              'objects/twitter-post/*',
                              'objects/url/*',
                              'objects/user-account/*',
                              'objects/vehicle/*',
                              'objects/victim/*',
                              'objects/virustotal-graph/*',
                              'objects/virustotal-report/*',
                              'objects/virustotal-submission/*',
                              'objects/vulnerability/*',
                              'objects/weakness/*',
                              'objects/whois/*',
                              'objects/windows-service/*',
                              'objects/x509/*',
                              'objects/yabin/*',
                              'objects/yara/*',
                              'objects/youtube-channel/*',
                              'objects/youtube-comment/*',
                              'objects/youtube-playlist/*',
                              'objects/youtube-video/*',
                              'relationships/*'],
 'pymisp.tools': ['pdf_fonts/*']}

install_requires = \
['deprecated>=1.2.13,<2.0.0',
 'jsonschema>=4.5.1,<5.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.27.1,<3.0.0']

extras_require = \
{'brotli': ['urllib3[brotli]>=1.26.9,<2.0.0'],
 'docs': ['sphinx-autodoc-typehints>=1.18.1,<2.0.0',
          'recommonmark>=0.7.1,<0.8.0'],
 'email': ['extract_msg>=0.30.13,<0.31.0',
           'RTFDE>=0.0.2,<0.0.3',
           'oletools>=0.60.1,<0.61.0'],
 'fileobjects': ['python-magic>=0.4.26,<0.5.0',
                 'pydeep2>=0.5.1,<0.6.0',
                 'lief>=0.12.1,<0.13.0'],
 'openioc': ['beautifulsoup4>=4.11.1,<5.0.0'],
 'pdfexport': ['reportlab>=3.6.9,<4.0.0'],
 'url': ['pyfaup>=1.2,<2.0', 'chardet>=4.0.0,<5.0.0'],
 'virustotal': ['validators>=0.19.0,<0.20.0']}

setup_kwargs = {
    'name': 'pymisp',
    'version': '2.4.159',
    'description': 'Python API for MISP.',
    'long_description': '**IMPORTANT NOTE**: This library will require **at least** python 3.8 starting the 1st of January 2022. If you have legacy versions of python, please use the latest PyMISP version that will be released in December 2021, and consider updating your system(s). Anything released within the last 2 years will do, starting with Ubuntu 20.04.\n\n# PyMISP - Python Library to access MISP\n\n[![Documentation Status](https://readthedocs.org/projects/pymisp/badge/?version=latest)](http://pymisp.readthedocs.io/?badge=latest)\n[![Coverage Status](https://coveralls.io/repos/github/MISP/PyMISP/badge.svg?branch=main)](https://coveralls.io/github/MISP/PyMISP?branch=main)\n[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)\n[![PyPi version](https://img.shields.io/pypi/v/pymisp.svg)](https://pypi.python.org/pypi/pymisp/)\n[![Number of PyPI downloads](https://img.shields.io/pypi/dm/pymisp.svg)](https://pypi.python.org/pypi/pymisp/)\n\nPyMISP is a Python library to access [MISP](https://github.com/MISP/MISP) platforms via their REST API.\n\nPyMISP allows you to fetch events, add or update events/attributes, add or update samples or search for attributes.\n\n## Install from pip\n\n**It is strongly recommended to use a virtual environment**\n\nIf you want to know more about virtual environments, [python has you covered](https://docs.python.org/3/tutorial/venv.html)\n\nOnly basic dependencies:\n```\npip3 install pymisp\n```\n\nAnd there are a few optional dependencies:\n* fileobjects: to create PE/ELF/Mach-o objects\n* openioc: to import files in OpenIOC format (not really maintained)\n* virustotal: to query VirusTotal and generate the appropriate objects\n* docs: to generate te documentation\n* pdfexport: to generate PDF reports out of MISP events\n* url: to generate URL objects out of URLs with Pyfaup\n* email: to generate MISP Email objects\n* brotli: to use the brotli compression when interacting with a MISP instance\n\nExample: \n\n```\npip3 install pymisp[virustotal,email]\n```\n\n## Install the latest version from repo from development purposes\n\n**Note**: poetry is required; e.g., "pip3 install poetry"\n\n```\ngit clone https://github.com/MISP/PyMISP.git && cd PyMISP\ngit submodule update --init\npoetry install -E fileobjects -E openioc -E virustotal -E docs -E pdfexport\n```\n\n### Running the tests\n\n```bash\npoetry run nosetests-3.4 --with-coverage --cover-package=pymisp,tests --cover-tests tests/test_*.py\n```\n\nIf you have a MISP instance to test against, you can also run the live ones:\n\n**Note**: You need to update the key in `tests/testlive_comprehensive.py` to the automation key of your admin account.\n\n```bash\npoetry run nosetests-3.4 --with-coverage --cover-package=pymisp,tests --cover-tests tests/testlive_comprehensive.py\n```\n\n## Samples and how to use PyMISP\n\nVarious examples and samples scripts are in the [examples/](examples/) directory.\n\nIn the examples directory, you will need to change the keys.py.sample to enter your MISP url and API key.\n\n```\ncd examples\ncp keys.py.sample keys.py\nvim keys.py\n```\n\nThe API key of MISP is available in the Automation section of the MISP web interface.\n\nTo test if your URL and API keys are correct, you can test with examples/last.py to\nfetch the events published in the last x amount of time (supported time indicators: days (d), hours (h) and minutes (m)).\nlast.py\n```\ncd examples\npython3 last.py -l 10h # 10 hours\npython3 last.py -l 5d  #  5 days\npython3 last.py -l 45m # 45 minutes\n```\n\n\n## Debugging\n\nYou have two options here:\n\n1. Pass `debug=True` to `PyMISP` and it will enable logging.DEBUG to stderr on the whole module\n\n2. Use the python logging module directly:\n\n```python\n\nimport logging\nlogger = logging.getLogger(\'pymisp\')\n\n# Configure it as you wish, for example, enable DEBUG mode:\nlogger.setLevel(logging.DEBUG)\n```\n\nOr if you want to write the debug output to a file instead of stderr:\n\n```python\nimport pymisp\nimport logging\n\nlogger = logging.getLogger(\'pymisp\')\nlogging.basicConfig(level=logging.DEBUG, filename="debug.log", filemode=\'w\', format=pymisp.FORMAT)\n```\n\n## Test cases\n\n1. The content of `mispevent.py` is tested on every commit\n2. The test cases that require a running MISP instance can be run the following way:\n\n\n```bash\n# From poetry\n\nnosetests-3.4 -s --with-coverage --cover-package=pymisp,tests --cover-tests tests/testlive_comprehensive.py:TestComprehensive.[test_name]\n\n```\n\n## Documentation\n\nThe documentation is available [here](https://pymisp.readthedocs.io/en/latest/).\n\n### Jupyter notebook\n\nA series of [Jupyter notebooks for PyMISP tutorial](https://github.com/MISP/PyMISP/tree/main/docs/tutorial) are available in the repository.\n\n## Everything is a Mutable Mapping\n\n... or at least everything that can be imported/exported from/to a json blob\n\n`AbstractMISP` is the master class, and inherits from `collections.MutableMapping` which means\nthe class can be represented as a python dictionary.\n\nThe abstraction assumes every property that should not be seen in the dictionary is prepended with a `_`,\nor its name is added to the private list `__not_jsonable` (accessible through `update_not_jsonable` and `set_not_jsonable`.\n\nThis master class has helpers that make it easy to load, and export to, and from, a json string.\n\n`MISPEvent`, `MISPAttribute`, `MISPObjectReference`, `MISPObjectAttribute`, and `MISPObject`\nare subclasses of AbstractMISP, which mean that they can be handled as python dictionaries.\n\n## MISP Objects\n\nCreating a new MISP object generator should be done using a pre-defined template and inherit `AbstractMISPObjectGenerator`.\n\nYour new MISPObject generator must generate attributes and add them as class properties using `add_attribute`.\n\nWhen the object is sent to MISP, all the class properties will be exported to the JSON export.\n\n# License\n\nPyMISP is distributed under an [open source license](./LICENSE). A simplified 2-BSD license.\n\n',
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MISP/PyMISP',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
