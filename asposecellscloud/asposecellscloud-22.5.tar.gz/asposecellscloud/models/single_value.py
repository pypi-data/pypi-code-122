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


class SingleValue(object):
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
        'value_type': 'ValueType',
        'value': 'str'
    }

    attribute_map = {
        'value_type': 'ValueType',
        'value': 'Value'
    }
    
    @staticmethod
    def get_swagger_types():
        return SingleValue.swagger_types
    
    @staticmethod
    def get_attribute_map():
        return SingleValue.attribute_map
    
    def get_from_container(self, attr):
        if attr in self.container:
            return self.container[attr]
        return None

    def __init__(self, value_type=None, value=None, **kw):
        """
        Associative dict for storing property values
        """
        self.container = {}
		    
        """
        SingleValue - a model defined in Swagger
        """

        self.container['value_type'] = None
        self.container['value'] = None

        if value_type is not None:
          self.value_type = value_type
        if value is not None:
          self.value = value

    @property
    def value_type(self):
        """
        Gets the value_type of this SingleValue.

        :return: The value_type of this SingleValue.
        :rtype: ValueType
        """
        return self.container['value_type']

    @value_type.setter
    def value_type(self, value_type):
        """
        Sets the value_type of this SingleValue.

        :param value_type: The value_type of this SingleValue.
        :type: ValueType
        """

        self.container['value_type'] = value_type

    @property
    def value(self):
        """
        Gets the value of this SingleValue.

        :return: The value of this SingleValue.
        :rtype: str
        """
        return self.container['value']

    @value.setter
    def value(self, value):
        """
        Sets the value of this SingleValue.

        :param value: The value of this SingleValue.
        :type: str
        """

        self.container['value'] = value

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
        if not isinstance(other, SingleValue):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
