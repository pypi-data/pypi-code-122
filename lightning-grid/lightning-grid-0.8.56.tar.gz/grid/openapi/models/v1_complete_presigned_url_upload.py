# coding: utf-8

"""
    external/v1/external_session_service.proto

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: version not set
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    NOTE
    ----
    standard swagger-codegen-cli for this python client has been modified
    by custom templates. The purpose of these templates is to include
    typing information in the API and Model code. Please refer to the
    main grid repository for more info
"""


import pprint
import re  # noqa: F401
from typing import TYPE_CHECKING

import six

from grid.openapi.configuration import Configuration

if TYPE_CHECKING:
    from datetime import datetime
    from grid.openapi.models import *

class V1CompletePresignedUrlUpload(object):
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
        'etag': 'str',
        'part_number': 'str'
    }

    attribute_map = {
        'etag': 'etag',
        'part_number': 'partNumber'
    }

    def __init__(self, etag: 'str' = None, part_number: 'str' = None, _configuration=None):  # noqa: E501
        """V1CompletePresignedUrlUpload - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._etag = None
        self._part_number = None
        self.discriminator = None

        if etag is not None:
            self.etag = etag
        if part_number is not None:
            self.part_number = part_number

    @property
    def etag(self) -> 'str':
        """Gets the etag of this V1CompletePresignedUrlUpload.  # noqa: E501


        :return: The etag of this V1CompletePresignedUrlUpload.  # noqa: E501
        :rtype: str
        """
        return self._etag

    @etag.setter
    def etag(self, etag: 'str'):
        """Sets the etag of this V1CompletePresignedUrlUpload.


        :param etag: The etag of this V1CompletePresignedUrlUpload.  # noqa: E501
        :type: str
        """

        self._etag = etag

    @property
    def part_number(self) -> 'str':
        """Gets the part_number of this V1CompletePresignedUrlUpload.  # noqa: E501


        :return: The part_number of this V1CompletePresignedUrlUpload.  # noqa: E501
        :rtype: str
        """
        return self._part_number

    @part_number.setter
    def part_number(self, part_number: 'str'):
        """Sets the part_number of this V1CompletePresignedUrlUpload.


        :param part_number: The part_number of this V1CompletePresignedUrlUpload.  # noqa: E501
        :type: str
        """

        self._part_number = part_number

    def to_dict(self) -> dict:
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
        if issubclass(V1CompletePresignedUrlUpload, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1CompletePresignedUrlUpload') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1CompletePresignedUrlUpload):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other: 'V1CompletePresignedUrlUpload') -> bool:
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1CompletePresignedUrlUpload):
            return True

        return self.to_dict() != other.to_dict()
