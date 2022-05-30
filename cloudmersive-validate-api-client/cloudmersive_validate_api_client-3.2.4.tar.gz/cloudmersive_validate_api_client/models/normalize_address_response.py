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


class NormalizeAddressResponse(object):
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
        'valid_address': 'bool',
        'building': 'str',
        'street_number': 'str',
        'street': 'str',
        'city': 'str',
        'state_or_province': 'str',
        'postal_code': 'str',
        'country_full_name': 'str',
        'iso_two_letter_code': 'str',
        'latitude': 'float',
        'longitude': 'float'
    }

    attribute_map = {
        'valid_address': 'ValidAddress',
        'building': 'Building',
        'street_number': 'StreetNumber',
        'street': 'Street',
        'city': 'City',
        'state_or_province': 'StateOrProvince',
        'postal_code': 'PostalCode',
        'country_full_name': 'CountryFullName',
        'iso_two_letter_code': 'ISOTwoLetterCode',
        'latitude': 'Latitude',
        'longitude': 'Longitude'
    }

    def __init__(self, valid_address=None, building=None, street_number=None, street=None, city=None, state_or_province=None, postal_code=None, country_full_name=None, iso_two_letter_code=None, latitude=None, longitude=None):  # noqa: E501
        """NormalizeAddressResponse - a model defined in Swagger"""  # noqa: E501

        self._valid_address = None
        self._building = None
        self._street_number = None
        self._street = None
        self._city = None
        self._state_or_province = None
        self._postal_code = None
        self._country_full_name = None
        self._iso_two_letter_code = None
        self._latitude = None
        self._longitude = None
        self.discriminator = None

        if valid_address is not None:
            self.valid_address = valid_address
        if building is not None:
            self.building = building
        if street_number is not None:
            self.street_number = street_number
        if street is not None:
            self.street = street
        if city is not None:
            self.city = city
        if state_or_province is not None:
            self.state_or_province = state_or_province
        if postal_code is not None:
            self.postal_code = postal_code
        if country_full_name is not None:
            self.country_full_name = country_full_name
        if iso_two_letter_code is not None:
            self.iso_two_letter_code = iso_two_letter_code
        if latitude is not None:
            self.latitude = latitude
        if longitude is not None:
            self.longitude = longitude

    @property
    def valid_address(self):
        """Gets the valid_address of this NormalizeAddressResponse.  # noqa: E501

        True if the address is valid, false otherwise  # noqa: E501

        :return: The valid_address of this NormalizeAddressResponse.  # noqa: E501
        :rtype: bool
        """
        return self._valid_address

    @valid_address.setter
    def valid_address(self, valid_address):
        """Sets the valid_address of this NormalizeAddressResponse.

        True if the address is valid, false otherwise  # noqa: E501

        :param valid_address: The valid_address of this NormalizeAddressResponse.  # noqa: E501
        :type: bool
        """

        self._valid_address = valid_address

    @property
    def building(self):
        """Gets the building of this NormalizeAddressResponse.  # noqa: E501

        The name of the building, house or structure if applicable, such as \"Cloudmersive Building 2\".  This will often by null.  # noqa: E501

        :return: The building of this NormalizeAddressResponse.  # noqa: E501
        :rtype: str
        """
        return self._building

    @building.setter
    def building(self, building):
        """Sets the building of this NormalizeAddressResponse.

        The name of the building, house or structure if applicable, such as \"Cloudmersive Building 2\".  This will often by null.  # noqa: E501

        :param building: The building of this NormalizeAddressResponse.  # noqa: E501
        :type: str
        """

        self._building = building

    @property
    def street_number(self):
        """Gets the street_number of this NormalizeAddressResponse.  # noqa: E501

        The street number or house number of the address.  For example, in the address \"1600 Pennsylvania Avenue NW\" the street number would be \"1600\".  This value will typically be populated for most addresses.  # noqa: E501

        :return: The street_number of this NormalizeAddressResponse.  # noqa: E501
        :rtype: str
        """
        return self._street_number

    @street_number.setter
    def street_number(self, street_number):
        """Sets the street_number of this NormalizeAddressResponse.

        The street number or house number of the address.  For example, in the address \"1600 Pennsylvania Avenue NW\" the street number would be \"1600\".  This value will typically be populated for most addresses.  # noqa: E501

        :param street_number: The street_number of this NormalizeAddressResponse.  # noqa: E501
        :type: str
        """

        self._street_number = street_number

    @property
    def street(self):
        """Gets the street of this NormalizeAddressResponse.  # noqa: E501

        The name of the street or road of the address.  For example, in the address \"1600 Pennsylvania Avenue NW\" the street number would be \"Pennsylvania Avenue NW\".  # noqa: E501

        :return: The street of this NormalizeAddressResponse.  # noqa: E501
        :rtype: str
        """
        return self._street

    @street.setter
    def street(self, street):
        """Sets the street of this NormalizeAddressResponse.

        The name of the street or road of the address.  For example, in the address \"1600 Pennsylvania Avenue NW\" the street number would be \"Pennsylvania Avenue NW\".  # noqa: E501

        :param street: The street of this NormalizeAddressResponse.  # noqa: E501
        :type: str
        """

        self._street = street

    @property
    def city(self):
        """Gets the city of this NormalizeAddressResponse.  # noqa: E501

        The city of the address.  # noqa: E501

        :return: The city of this NormalizeAddressResponse.  # noqa: E501
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this NormalizeAddressResponse.

        The city of the address.  # noqa: E501

        :param city: The city of this NormalizeAddressResponse.  # noqa: E501
        :type: str
        """

        self._city = city

    @property
    def state_or_province(self):
        """Gets the state_or_province of this NormalizeAddressResponse.  # noqa: E501

        The state or province of the address.  # noqa: E501

        :return: The state_or_province of this NormalizeAddressResponse.  # noqa: E501
        :rtype: str
        """
        return self._state_or_province

    @state_or_province.setter
    def state_or_province(self, state_or_province):
        """Sets the state_or_province of this NormalizeAddressResponse.

        The state or province of the address.  # noqa: E501

        :param state_or_province: The state_or_province of this NormalizeAddressResponse.  # noqa: E501
        :type: str
        """

        self._state_or_province = state_or_province

    @property
    def postal_code(self):
        """Gets the postal_code of this NormalizeAddressResponse.  # noqa: E501

        The postal code or zip code of the address.  # noqa: E501

        :return: The postal_code of this NormalizeAddressResponse.  # noqa: E501
        :rtype: str
        """
        return self._postal_code

    @postal_code.setter
    def postal_code(self, postal_code):
        """Sets the postal_code of this NormalizeAddressResponse.

        The postal code or zip code of the address.  # noqa: E501

        :param postal_code: The postal_code of this NormalizeAddressResponse.  # noqa: E501
        :type: str
        """

        self._postal_code = postal_code

    @property
    def country_full_name(self):
        """Gets the country_full_name of this NormalizeAddressResponse.  # noqa: E501

        Country of the address, if present in the address.  If not included in the address it will be null.  # noqa: E501

        :return: The country_full_name of this NormalizeAddressResponse.  # noqa: E501
        :rtype: str
        """
        return self._country_full_name

    @country_full_name.setter
    def country_full_name(self, country_full_name):
        """Sets the country_full_name of this NormalizeAddressResponse.

        Country of the address, if present in the address.  If not included in the address it will be null.  # noqa: E501

        :param country_full_name: The country_full_name of this NormalizeAddressResponse.  # noqa: E501
        :type: str
        """

        self._country_full_name = country_full_name

    @property
    def iso_two_letter_code(self):
        """Gets the iso_two_letter_code of this NormalizeAddressResponse.  # noqa: E501

        Two-letter ISO 3166-1 country code  # noqa: E501

        :return: The iso_two_letter_code of this NormalizeAddressResponse.  # noqa: E501
        :rtype: str
        """
        return self._iso_two_letter_code

    @iso_two_letter_code.setter
    def iso_two_letter_code(self, iso_two_letter_code):
        """Sets the iso_two_letter_code of this NormalizeAddressResponse.

        Two-letter ISO 3166-1 country code  # noqa: E501

        :param iso_two_letter_code: The iso_two_letter_code of this NormalizeAddressResponse.  # noqa: E501
        :type: str
        """

        self._iso_two_letter_code = iso_two_letter_code

    @property
    def latitude(self):
        """Gets the latitude of this NormalizeAddressResponse.  # noqa: E501

        If the address is valid, the degrees latitude of the validated address, null otherwise  # noqa: E501

        :return: The latitude of this NormalizeAddressResponse.  # noqa: E501
        :rtype: float
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude):
        """Sets the latitude of this NormalizeAddressResponse.

        If the address is valid, the degrees latitude of the validated address, null otherwise  # noqa: E501

        :param latitude: The latitude of this NormalizeAddressResponse.  # noqa: E501
        :type: float
        """

        self._latitude = latitude

    @property
    def longitude(self):
        """Gets the longitude of this NormalizeAddressResponse.  # noqa: E501

        If the address is valid, the degrees longitude of the validated address, null otherwise  # noqa: E501

        :return: The longitude of this NormalizeAddressResponse.  # noqa: E501
        :rtype: float
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude):
        """Sets the longitude of this NormalizeAddressResponse.

        If the address is valid, the degrees longitude of the validated address, null otherwise  # noqa: E501

        :param longitude: The longitude of this NormalizeAddressResponse.  # noqa: E501
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
        if issubclass(NormalizeAddressResponse, dict):
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
        if not isinstance(other, NormalizeAddressResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
