from utils import parse, dump_str
from xmapper import Comparer
from lxml import etree
from pprint import pprint


attr_qname = etree.QName("http://www.w3.org/2001/XMLSchema-instance", "schemaLocation")

# root = etree.Element('ClinicalDocument',
#                      {attr_qname: 'urn:hl7-org:v3 CDA.xsd'},
#                      nsmap={None: 'urn:hl7-org:v3',
#                             'mif': 'urn:hl7-org:v3/mif',
#                             'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
#                             })
#
# pprint(etree.tostring(root))

project = etree.Element('project',
                     {attr_qname: 'http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd'},
                     nsmap={None: 'http://maven.apache.org/POM/4.0.0',
                            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
                            })

pprint(etree.tostring(project))

