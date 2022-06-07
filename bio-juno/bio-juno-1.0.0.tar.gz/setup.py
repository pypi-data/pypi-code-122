# -*- coding: utf-8 -*-
import atexit
from setuptools import setup
from setuptools.command.install import install as SetuptoolsInstall
from juno.config import _post_install
        
class MakeInstall(SetuptoolsInstall):
    def __init__(self, *args, **kwargs):
        super(MakeInstall, self).__init__(*args, **kwargs)
        atexit.register(_post_install)


packages = \
['juno']

package_data = \
{'': ['*'], 'juno': ['data/*', 'tools/*']}

install_requires = \
['pysradb>=1.3.0,<2.0.0',
 'streamlit-aggrid>=0.2.3,<0.3.0',
 'streamlit>=1.9.2,<2.0.0']

entry_points = \
{'console_scripts': ['juno = juno.cli:main']}

setup_kwargs = {
    'name': 'bio-juno',
    'version': '1.0.0',
    'description': 'Juno: read data generator',
    'long_description': '# Juno: read data generator  \n\nJuno have two methods to generate reads fastq.  \n1. Download the real fastq submitted to NCBI SRA from the contributors\n2. Simulate the "fake" fastq   \n\nIf you want to develope genomic tools but has no real data, juno can generate the read fastq for your testing.\n\nJuno is also available as a public online resource: https://juno.hlin.tw\n\n## Requirements  \n- Linux \n- Python >= 3.6\n \n## Installation  \n\n### Pypi version \nhttps://pypi.org/project/juno/\n```\npip install juno\n```\n\n### Intall from source  \n\n```\ngit clone https://github.com/hunglin59638/juno.git\ncd juno\npython3 setup.py install\n```\n\n## CLI  \n```\njuno -h \nusage: juno [-h] SUBCOMMAND ...\n\nJuno: read data generator\n\noptional arguments:\n  -h, --help  show this help message and exit\n\nsubcommands:\n  subcommands\n\n  SUBCOMMAND\n    sra       Download reads from SRA database\n    simulate  Simulating reads by reference genome\n```\n### Download reads from SRA database  \n```\njuno sra -a SRR19400588 -o /path/to/directory\n```\n\n### Simulate reads fastq  \nThere are two way to simulate read fastq    \n1. Input your genome fasta\n```\njuno simulate -r /your/genome/fasta -o /path/to/directory --compressed --depth 200\n```\n2. Input RefSeq assembly accession and its genome will be downloaded from NCBI\n```\njuno simulate -a GCF_002004995.1 -o /path/to/directory --compressed --depth 200\n```\nTips:\ndepth is greater than 200x is the better parameter for bacteria\n\n### Update local NCBI RefSeq assembly summary  \n```\njuno simulate --update\n```\n\n## Python API\n\n### Use Case: Update NCBI RefSeq Assembly Summary and get it in local \n\n```\nfrom juno.data import Assembly\nassembly = Assembly()\nassembly.update_assembly()\ndf = assembly.dataframe\ndf.head()\n```\n```\n\tassembly_accession\tbioproject\tbiosample\twgs_master\trefseq_category\ttaxid\tspecies_taxid\torganism_name\tinfraspecific_name\tisolate\tversion_status\tassembly_level\trelease_type\tgenome_rep\tseq_rel_date\tasm_name\tsubmitter\tgbrs_paired_asm\n0\tGCF_000001215.4\tPRJNA164\tSAMN02803731\t\treference genome\t7227\t7227\tDrosophila melanogaster\t\t\tlatest\tChromosome\tMajor\tFull\t2014/08/01\tRelease 6 plus ISO1 MT\tThe FlyBase Consortium/Berkeley Drosophila Genome Project/Celera Genomics\tGCA_000001215.4\n1\tGCF_000001405.40\tPRJNA168\t\t\treference genome\t9606\t9606\tHomo sapiens\t\t\tlatest\tChromosome\tPatch\tFull\t2022/02/03\tGRCh38.p14\tGenome Reference Consortium\tGCA_000001405.29\n2\tGCF_000001635.27\tPRJNA169\t\t\treference genome\t10090\t10090\tMus musculus\t\t\tlatest\tChromosome\tMajor\tFull\t2020/06/24\tGRCm39\tGenome Reference Consortium\tGCA_000001635.9\n3\tGCF_000001735.4\tPRJNA116\tSAMN03081427\t\treference genome\t3702\t3702\tArabidopsis thaliana\tecotype=Columbia\t\tlatest\tChromosome\tMinor\tFull\t2018/03/15\tTAIR10.1\tThe Arabidopsis Information Resource (TAIR)\tGCA_000001735.2\n4\tGCF_000001905.1\tPRJNA70973\tSAMN02953622\tAAGU00000000.3\trepresentative genome\t9785\t9785\tLoxodonta africana\t\tISIS603380\tlatest\tScaffold\tMajor\tFull\t2009/07/15\tLoxafr3.0\tBroad Institute\tGCA_000001905.1\n\n```\n\n### Use Case: Download assembly genome  \n```\nfrom juno.data import Assembly\nassembly = Assembly()\ngenome_path = assembly.download("GCF_002004995.1", "/your/output/directory")\n```\n### Use Case: Simulate reads from genome reference  \n```\nfrom juno.simulator import Simulator\nsm = Simulator\n```\n\n## Citation\n\n- pysradb: A Python package to query next-generation sequencing metadata and data from NCBI Sequence Read Archive (https://f1000research.com/articles/8-532/v1)  \n- PBSIM2: a simulator for long-read sequencers with a novel generative model of quality scores (https://doi.org/10.1093/bioinformatics/btaa835)\n',
    'long_description_content_type': 'text/markdown',
    'author': 'hunglin',
    'author_email': 'hunglin59638@gmail.com',
    'maintainer': 'hunglin',
    'maintainer_email': 'hunglin59638@gmail.com',
    'url': 'https://github.com/hunglin59638/juno',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
    'cmdclass': {'install' : MakeInstall}
}


setup(**setup_kwargs)


