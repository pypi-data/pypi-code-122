import os
from io import BufferedIOBase
from xml.sax import parse, parseString
from typing import Union
from drb import DrbNode
from drb.factory.factory import DrbFactory
from drb.exceptions import DrbFactoryException

from .xml_node import XmlBaseNode, SaxNodeHandler


class XmlNodeFactory(DrbFactory):
    def _create(self, node: DrbNode) -> DrbNode:
        if node.has_impl(BufferedIOBase):
            return XmlBaseNode(node, node.get_impl(BufferedIOBase))

    def create(self, source: Union[DrbNode, str]) -> DrbNode:
        if isinstance(source, str):
            handler = SaxNodeHandler()
            if os.path.exists(source):
                parse(source, handler)
            else:
                parseString(source, handler)
            return handler.get_node()
        elif isinstance(source, DrbNode):
            return self._create(source)
        raise DrbFactoryException(f'Invalid parameter type: {type(source)}')
