# coding: utf-8

"""
Copyright (c) 2022 Aspose.Cells Cloud
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
"""


from pprint import pformat
from six import iteritems
import re


class CellValue(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'row_index': 'int',
        'column_index': 'int',
        'style': 'Style',
        'type': 'str',
        'value': 'str',
        'formula': 'str'
    }

    attribute_map = {
        'row_index': 'rowIndex',
        'column_index': 'columnIndex',
        'style': 'style',
        'type': 'type',
        'value': 'value',
        'formula': 'formula'
    }
    
    @staticmethod
    def get_swagger_types():
        return CellValue.swagger_types
    
    @staticmethod
    def get_attribute_map():
        return CellValue.attribute_map
    
    def get_from_container(self, attr):
        if attr in self.container:
            return self.container[attr]
        return None

    def __init__(self, row_index=None, column_index=None, style=None, type=None, value=None, formula=None, **kw):
        """
        Associative dict for storing property values
        """
        self.container = {}
		    
        """
        CellValue - a model defined in Swagger
        """

        self.container['row_index'] = None
        self.container['column_index'] = None
        self.container['style'] = None
        self.container['type'] = None
        self.container['value'] = None
        self.container['formula'] = None

        if row_index is not None:
          self.row_index = row_index
        if column_index is not None:
          self.column_index = column_index
        if style is not None:
          self.style = style
        if type is not None:
          self.type = type
        if value is not None:
          self.value = value
        if formula is not None:
          self.formula = formula

    @property
    def row_index(self):
        """
        Gets the row_index of this CellValue.

        :return: The row_index of this CellValue.
        :rtype: int
        """
        return self.container['row_index']

    @row_index.setter
    def row_index(self, row_index):
        """
        Sets the row_index of this CellValue.

        :param row_index: The row_index of this CellValue.
        :type: int
        """

        self.container['row_index'] = row_index

    @property
    def column_index(self):
        """
        Gets the column_index of this CellValue.

        :return: The column_index of this CellValue.
        :rtype: int
        """
        return self.container['column_index']

    @column_index.setter
    def column_index(self, column_index):
        """
        Sets the column_index of this CellValue.

        :param column_index: The column_index of this CellValue.
        :type: int
        """

        self.container['column_index'] = column_index

    @property
    def style(self):
        """
        Gets the style of this CellValue.

        :return: The style of this CellValue.
        :rtype: Style
        """
        return self.container['style']

    @style.setter
    def style(self, style):
        """
        Sets the style of this CellValue.

        :param style: The style of this CellValue.
        :type: Style
        """

        self.container['style'] = style

    @property
    def type(self):
        """
        Gets the type of this CellValue.

        :return: The type of this CellValue.
        :rtype: str
        """
        return self.container['type']

    @type.setter
    def type(self, type):
        """
        Sets the type of this CellValue.

        :param type: The type of this CellValue.
        :type: str
        """

        self.container['type'] = type

    @property
    def value(self):
        """
        Gets the value of this CellValue.

        :return: The value of this CellValue.
        :rtype: str
        """
        return self.container['value']

    @value.setter
    def value(self, value):
        """
        Sets the value of this CellValue.

        :param value: The value of this CellValue.
        :type: str
        """

        self.container['value'] = value

    @property
    def formula(self):
        """
        Gets the formula of this CellValue.

        :return: The formula of this CellValue.
        :rtype: str
        """
        return self.container['formula']

    @formula.setter
    def formula(self, formula):
        """
        Sets the formula of this CellValue.

        :param formula: The formula of this CellValue.
        :type: str
        """

        self.container['formula'] = formula

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.get_swagger_types()):
            value = self.get_from_container(attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, CellValue):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
