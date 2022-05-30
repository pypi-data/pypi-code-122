import os
import sys

from setuptools import find_packages
from setuptools import setup

version = '1.0.1'

install_requires = [
    'cloudflare>=1.5.1',
    'setuptools>=41.6.0',
    'dnspython>=2.2.0',
]

if not os.environ.get('SNAP_BUILD'):
    install_requires.extend([
        # We specify the minimum acme and certbot version as the current plugin
        # version for simplicity. See
        # https://github.com/certbot/certbot/issues/8761 for more info.
        f'acme>={version}',
        f'certbot>={version}',
    ])
elif 'bdist_wheel' in sys.argv[1:]:
    raise RuntimeError('Unset SNAP_BUILD when building wheels '
                       'to include certbot dependencies.')
if os.environ.get('SNAP_BUILD'):
    install_requires.append('packaging')

setup(
    name='certbot-dns-cloudflare-cname',
    version=version,
    description="Cloudflare DNS Authenticator plugin for Certbot with CNAME support.",
    url='https://github.com/rsc-dev/certbot-dns-cloudflare-cname',
    author="Radoslaw Matusiak",
    author_email='radoslaw.matusiak@gmail.com',
    license='Apache License 2.0',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Installation/Setup',
        'Topic :: System :: Networking',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'certbot.plugins': [
            'dns-cloudflare-cname = certbot_dns_cloudflare_cname._internal.dns_cloudflare_cname:Authenticator',
        ],
    },
)
