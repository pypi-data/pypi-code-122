# coding: utf-8

"""
    validateapi

    The validation APIs help you validate data. Check if an E-mail address is real. Check if a domain is real. Check up on an IP address, and even where it is located. All this and much more is available in the validation API.  # noqa: E501

    OpenAPI spec version: v1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class UrlSsrfResponseBatch(object):
    """NOTE: This class is auto generated by the swagger code generator program.

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
        'output_items': 'list[UrlSsrfResponseFull]'
    }

    attribute_map = {
        'output_items': 'OutputItems'
    }

    def __init__(self, output_items=None):  # noqa: E501
        """UrlSsrfResponseBatch - a model defined in Swagger"""  # noqa: E501

        self._output_items = None
        self.discriminator = None

        if output_items is not None:
            self.output_items = output_items

    @property
    def output_items(self):
        """Gets the output_items of this UrlSsrfResponseBatch.  # noqa: E501

        Results of the operation, with indexes matched to input values  # noqa: E501

        :return: The output_items of this UrlSsrfResponseBatch.  # noqa: E501
        :rtype: list[UrlSsrfResponseFull]
        """
        return self._output_items

    @output_items.setter
    def output_items(self, output_items):
        """Sets the output_items of this UrlSsrfResponseBatch.

        Results of the operation, with indexes matched to input values  # noqa: E501

        :param output_items: The output_items of this UrlSsrfResponseBatch.  # noqa: E501
        :type: list[UrlSsrfResponseFull]
        """

        self._output_items = output_items

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
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
        if issubclass(UrlSsrfResponseBatch, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UrlSsrfResponseBatch):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
