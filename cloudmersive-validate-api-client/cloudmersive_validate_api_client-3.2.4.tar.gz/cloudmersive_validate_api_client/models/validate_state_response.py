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


class ValidateStateResponse(object):
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
        'valid_state': 'bool',
        'state_or_province': 'str',
        'latitude': 'float',
        'longitude': 'float'
    }

    attribute_map = {
        'valid_state': 'ValidState',
        'state_or_province': 'StateOrProvince',
        'latitude': 'Latitude',
        'longitude': 'Longitude'
    }

    def __init__(self, valid_state=None, state_or_province=None, latitude=None, longitude=None):  # noqa: E501
        """ValidateStateResponse - a model defined in Swagger"""  # noqa: E501

        self._valid_state = None
        self._state_or_province = None
        self._latitude = None
        self._longitude = None
        self.discriminator = None

        if valid_state is not None:
            self.valid_state = valid_state
        if state_or_province is not None:
            self.state_or_province = state_or_province
        if latitude is not None:
            self.latitude = latitude
        if longitude is not None:
            self.longitude = longitude

    @property
    def valid_state(self):
        """Gets the valid_state of this ValidateStateResponse.  # noqa: E501

        True if the address is valid, false otherwise  # noqa: E501

        :return: The valid_state of this ValidateStateResponse.  # noqa: E501
        :rtype: bool
        """
        return self._valid_state

    @valid_state.setter
    def valid_state(self, valid_state):
        """Sets the valid_state of this ValidateStateResponse.

        True if the address is valid, false otherwise  # noqa: E501

        :param valid_state: The valid_state of this ValidateStateResponse.  # noqa: E501
        :type: bool
        """

        self._valid_state = valid_state

    @property
    def state_or_province(self):
        """Gets the state_or_province of this ValidateStateResponse.  # noqa: E501

        If valid; State or province corresponding to the input state name, such as 'CA' or 'California'  # noqa: E501

        :return: The state_or_province of this ValidateStateResponse.  # noqa: E501
        :rtype: str
        """
        return self._state_or_province

    @state_or_province.setter
    def state_or_province(self, state_or_province):
        """Sets the state_or_province of this ValidateStateResponse.

        If valid; State or province corresponding to the input state name, such as 'CA' or 'California'  # noqa: E501

        :param state_or_province: The state_or_province of this ValidateStateResponse.  # noqa: E501
        :type: str
        """

        self._state_or_province = state_or_province

    @property
    def latitude(self):
        """Gets the latitude of this ValidateStateResponse.  # noqa: E501

        If the postal code is valid, the degrees latitude of the centroid of the state, null otherwise  # noqa: E501

        :return: The latitude of this ValidateStateResponse.  # noqa: E501
        :rtype: float
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        """Sets the latitude of this ValidateStateResponse.

        If the postal code is valid, the degrees latitude of the centroid of the state, null otherwise  # noqa: E501

        :param latitude: The latitude of this ValidateStateResponse.  # noqa: E501
        :type: float
        """

        self._latitude = latitude

    @property
    def longitude(self):
        """Gets the longitude of this ValidateStateResponse.  # noqa: E501

        If the postal code is valid, the degrees longitude of the centroid of the state, null otherwise  # noqa: E501

        :return: The longitude of this ValidateStateResponse.  # noqa: E501
        :rtype: float
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        """Sets the longitude of this ValidateStateResponse.

        If the postal code is valid, the degrees longitude of the centroid of the state, null otherwise  # noqa: E501

        :param longitude: The longitude of this ValidateStateResponse.  # noqa: E501
        :type: float
        """

        self._longitude = longitude

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
        if issubclass(ValidateStateResponse, dict):
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
        if not isinstance(other, ValidateStateResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
