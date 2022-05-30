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


class VatLookupResponse(object):
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
        'country_code': 'str',
        'vat_number': 'str',
        'is_valid': 'bool',
        'business_name': 'str',
        'business_address': 'str',
        'business_building': 'str',
        'business_street_number': 'str',
        'business_street': 'str',
        'business_city': 'str',
        'business_state_or_province': 'str',
        'business_postal_code': 'str',
        'business_country': 'str'
    }

    attribute_map = {
        'country_code': 'CountryCode',
        'vat_number': 'VatNumber',
        'is_valid': 'IsValid',
        'business_name': 'BusinessName',
        'business_address': 'BusinessAddress',
        'business_building': 'BusinessBuilding',
        'business_street_number': 'BusinessStreetNumber',
        'business_street': 'BusinessStreet',
        'business_city': 'BusinessCity',
        'business_state_or_province': 'BusinessStateOrProvince',
        'business_postal_code': 'BusinessPostalCode',
        'business_country': 'BusinessCountry'
    }

    def __init__(self, country_code=None, vat_number=None, is_valid=None, business_name=None, business_address=None, business_building=None, business_street_number=None, business_street=None, business_city=None, business_state_or_province=None, business_postal_code=None, business_country=None):  # noqa: E501
        """VatLookupResponse - a model defined in Swagger"""  # noqa: E501

        self._country_code = None
        self._vat_number = None
        self._is_valid = None
        self._business_name = None
        self._business_address = None
        self._business_building = None
        self._business_street_number = None
        self._business_street = None
        self._business_city = None
        self._business_state_or_province = None
        self._business_postal_code = None
        self._business_country = None
        self.discriminator = None

        if country_code is not None:
            self.country_code = country_code
        if vat_number is not None:
            self.vat_number = vat_number
        if is_valid is not None:
            self.is_valid = is_valid
        if business_name is not None:
            self.business_name = business_name
        if business_address is not None:
            self.business_address = business_address
        if business_building is not None:
            self.business_building = business_building
        if business_street_number is not None:
            self.business_street_number = business_street_number
        if business_street is not None:
            self.business_street = business_street
        if business_city is not None:
            self.business_city = business_city
        if business_state_or_province is not None:
            self.business_state_or_province = business_state_or_province
        if business_postal_code is not None:
            self.business_postal_code = business_postal_code
        if business_country is not None:
            self.business_country = business_country

    @property
    def country_code(self):
        """Gets the country_code of this VatLookupResponse.  # noqa: E501

        Two-letter country code  # noqa: E501

        :return: The country_code of this VatLookupResponse.  # noqa: E501
        :rtype: str
        """
        return self._country_code

    @country_code.setter
    def country_code(self, country_code):
        """Sets the country_code of this VatLookupResponse.

        Two-letter country code  # noqa: E501

        :param country_code: The country_code of this VatLookupResponse.  # noqa: E501
        :type: str
        """

        self._country_code = country_code

    @property
    def vat_number(self):
        """Gets the vat_number of this VatLookupResponse.  # noqa: E501

        VAT number  # noqa: E501

        :return: The vat_number of this VatLookupResponse.  # noqa: E501
        :rtype: str
        """
        return self._vat_number

    @vat_number.setter
    def vat_number(self, vat_number):
        """Sets the vat_number of this VatLookupResponse.

        VAT number  # noqa: E501

        :param vat_number: The vat_number of this VatLookupResponse.  # noqa: E501
        :type: str
        """

        self._vat_number = vat_number

    @property
    def is_valid(self):
        """Gets the is_valid of this VatLookupResponse.  # noqa: E501

        True if the VAT code is valid, false otherwise  # noqa: E501

        :return: The is_valid of this VatLookupResponse.  # noqa: E501
        :rtype: bool
        """
        return self._is_valid

    @is_valid.setter
    def is_valid(self, is_valid):
        """Sets the is_valid of this VatLookupResponse.

        True if the VAT code is valid, false otherwise  # noqa: E501

        :param is_valid: The is_valid of this VatLookupResponse.  # noqa: E501
        :type: bool
        """

        self._is_valid = is_valid

    @property
    def business_name(self):
        """Gets the business_name of this VatLookupResponse.  # noqa: E501

        Name of the business  # noqa: E501

        :return: The business_name of this VatLookupResponse.  # noqa: E501
        :rtype: str
        """
        return self._business_name

    @business_name.setter
    def business_name(self, business_name):
        """Sets the business_name of this VatLookupResponse.

        Name of the business  # noqa: E501

        :param business_name: The business_name of this VatLookupResponse.  # noqa: E501
        :type: str
        """

        self._business_name = business_name

    @property
    def business_address(self):
        """Gets the business_address of this VatLookupResponse.  # noqa: E501

        Business address as a single string  # noqa: E501

        :return: The business_address of this VatLookupResponse.  # noqa: E501
        :rtype: str
        """
        return self._business_address

    @business_address.setter
    def business_address(self, business_address):
        """Sets the business_address of this VatLookupResponse.

        Business address as a single string  # noqa: E501

        :param business_address: The business_address of this VatLookupResponse.  # noqa: E501
        :type: str
        """

        self._business_address = business_address

    @property
    def business_building(self):
        """Gets the business_building of this VatLookupResponse.  # noqa: E501

        For the business address, the name of the building, house or structure if applicable, such as \"Cloudmersive Building 2\".  This will often by null.  # noqa: E501

        :return: The business_building of this VatLookupResponse.  # noqa: E501
        :rtype: str
        """
        return self._business_building

    @business_building.setter
    def business_building(self, business_building):
        """Sets the business_building of this VatLookupResponse.

        For the business address, the name of the building, house or structure if applicable, such as \"Cloudmersive Building 2\".  This will often by null.  # noqa: E501

        :param business_building: The business_building of this VatLookupResponse.  # noqa: E501
        :type: str
        """

        self._business_building = business_building

    @property
    def business_street_number(self):
        """Gets the business_street_number of this VatLookupResponse.  # noqa: E501

        For the business address, the street number or house number of the address.  For example, in the address \"1600 Pennsylvania Avenue NW\" the street number would be \"1600\".  This value will typically be populated for most addresses.  # noqa: E501

        :return: The business_street_number of this VatLookupResponse.  # noqa: E501
        :rtype: str
        """
        return self._business_street_number

    @business_street_number.setter
    def business_street_number(self, business_street_number):
        """Sets the business_street_number of this VatLookupResponse.

        For the business address, the street number or house number of the address.  For example, in the address \"1600 Pennsylvania Avenue NW\" the street number would be \"1600\".  This value will typically be populated for most addresses.  # noqa: E501

        :param business_street_number: The business_street_number of this VatLookupResponse.  # noqa: E501
        :type: str
        """

        self._business_street_number = business_street_number

    @property
    def business_street(self):
        """Gets the business_street of this VatLookupResponse.  # noqa: E501

        For the business address, the name of the street or road of the address.  For example, in the address \"1600 Pennsylvania Avenue NW\" the street number would be \"Pennsylvania Avenue NW\".  # noqa: E501

        :return: The business_street of this VatLookupResponse.  # noqa: E501
        :rtype: str
        """
        return self._business_street

    @business_street.setter
    def business_street(self, business_street):
        """Sets the business_street of this VatLookupResponse.

        For the business address, the name of the street or road of the address.  For example, in the address \"1600 Pennsylvania Avenue NW\" the street number would be \"Pennsylvania Avenue NW\".  # noqa: E501

        :param business_street: The business_street of this VatLookupResponse.  # noqa: E501
        :type: str
        """

        self._business_street = business_street

    @property
    def business_city(self):
        """Gets the business_city of this VatLookupResponse.  # noqa: E501

        For the business address, the city of the address.  # noqa: E501

        :return: The business_city of this VatLookupResponse.  # noqa: E501
        :rtype: str
        """
        return self._business_city

    @business_city.setter
    def business_city(self, business_city):
        """Sets the business_city of this VatLookupResponse.

        For the business address, the city of the address.  # noqa: E501

        :param business_city: The business_city of this VatLookupResponse.  # noqa: E501
        :type: str
        """

        self._business_city = business_city

    @property
    def business_state_or_province(self):
        """Gets the business_state_or_province of this VatLookupResponse.  # noqa: E501

        For the business address, the state or province of the address.  # noqa: E501

        :return: The business_state_or_province of this VatLookupResponse.  # noqa: E501
        :rtype: str
        """
        return self._business_state_or_province

    @business_state_or_province.setter
    def business_state_or_province(self, business_state_or_province):
        """Sets the business_state_or_province of this VatLookupResponse.

        For the business address, the state or province of the address.  # noqa: E501

        :param business_state_or_province: The business_state_or_province of this VatLookupResponse.  # noqa: E501
        :type: str
        """

        self._business_state_or_province = business_state_or_province

    @property
    def business_postal_code(self):
        """Gets the business_postal_code of this VatLookupResponse.  # noqa: E501

        For the business address, the postal code or zip code of the address.  # noqa: E501

        :return: The business_postal_code of this VatLookupResponse.  # noqa: E501
        :rtype: str
        """
        return self._business_postal_code

    @business_postal_code.setter
    def business_postal_code(self, business_postal_code):
        """Sets the business_postal_code of this VatLookupResponse.

        For the business address, the postal code or zip code of the address.  # noqa: E501

        :param business_postal_code: The business_postal_code of this VatLookupResponse.  # noqa: E501
        :type: str
        """

        self._business_postal_code = business_postal_code

    @property
    def business_country(self):
        """Gets the business_country of this VatLookupResponse.  # noqa: E501

        For the business address, country of the address, if present in the address.  If not included in the address it will be null.  # noqa: E501

        :return: The business_country of this VatLookupResponse.  # noqa: E501
        :rtype: str
        """
        return self._business_country

    @business_country.setter
    def business_country(self, business_country):
        """Sets the business_country of this VatLookupResponse.

        For the business address, country of the address, if present in the address.  If not included in the address it will be null.  # noqa: E501

        :param business_country: The business_country of this VatLookupResponse.  # noqa: E501
        :type: str
        """

        self._business_country = business_country

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
        if issubclass(VatLookupResponse, dict):
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
        if not isinstance(other, VatLookupResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
