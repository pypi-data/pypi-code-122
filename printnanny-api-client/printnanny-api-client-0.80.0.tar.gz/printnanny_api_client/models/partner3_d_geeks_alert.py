# coding: utf-8

"""
    printnanny-api-client

    Official API client library forprintnanny.ai print-nanny.com  # noqa: E501

    The version of the OpenAPI document: 0.0.0
    Contact: leigh@printnanny.ai
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from printnanny_api_client.configuration import Configuration


class Partner3DGeeksAlert(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'event': 'str',
        'token': 'str',
        'printer': 'str',
        '_print': 'str',
        'current_time': 'int',
        'time_left': 'int',
        'percent': 'int',
        'image': 'str',
        'action': 'str'
    }

    attribute_map = {
        'event': 'event',
        'token': 'token',
        'printer': 'printer',
        '_print': 'print',
        'current_time': 'currentTime',
        'time_left': 'timeLeft',
        'percent': 'percent',
        'image': 'image',
        'action': 'action'
    }

    def __init__(self, event=None, token=None, printer=None, _print=None, current_time=None, time_left=None, percent=None, image=None, action=None, local_vars_configuration=None):  # noqa: E501
        """Partner3DGeeksAlert - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._event = None
        self._token = None
        self._printer = None
        self.__print = None
        self._current_time = None
        self._time_left = None
        self._percent = None
        self._image = None
        self._action = None
        self.discriminator = None

        self.event = event
        self.token = token
        self.printer = printer
        self._print = _print
        self.current_time = current_time
        self.time_left = time_left
        self.percent = percent
        self.image = image
        self.action = action

    @property
    def event(self):
        """Gets the event of this Partner3DGeeksAlert.  # noqa: E501


        :return: The event of this Partner3DGeeksAlert.  # noqa: E501
        :rtype: str
        """
        return self._event

    @event.setter
    def event(self, event):
        """Sets the event of this Partner3DGeeksAlert.


        :param event: The event of this Partner3DGeeksAlert.  # noqa: E501
        :type event: str
        """
        if self.local_vars_configuration.client_side_validation and event is None:  # noqa: E501
            raise ValueError("Invalid value for `event`, must not be `None`")  # noqa: E501

        self._event = event

    @property
    def token(self):
        """Gets the token of this Partner3DGeeksAlert.  # noqa: E501


        :return: The token of this Partner3DGeeksAlert.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this Partner3DGeeksAlert.


        :param token: The token of this Partner3DGeeksAlert.  # noqa: E501
        :type token: str
        """
        if self.local_vars_configuration.client_side_validation and token is None:  # noqa: E501
            raise ValueError("Invalid value for `token`, must not be `None`")  # noqa: E501

        self._token = token

    @property
    def printer(self):
        """Gets the printer of this Partner3DGeeksAlert.  # noqa: E501


        :return: The printer of this Partner3DGeeksAlert.  # noqa: E501
        :rtype: str
        """
        return self._printer

    @printer.setter
    def printer(self, printer):
        """Sets the printer of this Partner3DGeeksAlert.


        :param printer: The printer of this Partner3DGeeksAlert.  # noqa: E501
        :type printer: str
        """
        if self.local_vars_configuration.client_side_validation and printer is None:  # noqa: E501
            raise ValueError("Invalid value for `printer`, must not be `None`")  # noqa: E501

        self._printer = printer

    @property
    def _print(self):
        """Gets the _print of this Partner3DGeeksAlert.  # noqa: E501


        :return: The _print of this Partner3DGeeksAlert.  # noqa: E501
        :rtype: str
        """
        return self.__print

    @_print.setter
    def _print(self, _print):
        """Sets the _print of this Partner3DGeeksAlert.


        :param _print: The _print of this Partner3DGeeksAlert.  # noqa: E501
        :type _print: str
        """
        if self.local_vars_configuration.client_side_validation and _print is None:  # noqa: E501
            raise ValueError("Invalid value for `_print`, must not be `None`")  # noqa: E501

        self.__print = _print

    @property
    def current_time(self):
        """Gets the current_time of this Partner3DGeeksAlert.  # noqa: E501


        :return: The current_time of this Partner3DGeeksAlert.  # noqa: E501
        :rtype: int
        """
        return self._current_time

    @current_time.setter
    def current_time(self, current_time):
        """Sets the current_time of this Partner3DGeeksAlert.


        :param current_time: The current_time of this Partner3DGeeksAlert.  # noqa: E501
        :type current_time: int
        """
        if self.local_vars_configuration.client_side_validation and current_time is None:  # noqa: E501
            raise ValueError("Invalid value for `current_time`, must not be `None`")  # noqa: E501

        self._current_time = current_time

    @property
    def time_left(self):
        """Gets the time_left of this Partner3DGeeksAlert.  # noqa: E501


        :return: The time_left of this Partner3DGeeksAlert.  # noqa: E501
        :rtype: int
        """
        return self._time_left

    @time_left.setter
    def time_left(self, time_left):
        """Sets the time_left of this Partner3DGeeksAlert.


        :param time_left: The time_left of this Partner3DGeeksAlert.  # noqa: E501
        :type time_left: int
        """
        if self.local_vars_configuration.client_side_validation and time_left is None:  # noqa: E501
            raise ValueError("Invalid value for `time_left`, must not be `None`")  # noqa: E501

        self._time_left = time_left

    @property
    def percent(self):
        """Gets the percent of this Partner3DGeeksAlert.  # noqa: E501


        :return: The percent of this Partner3DGeeksAlert.  # noqa: E501
        :rtype: int
        """
        return self._percent

    @percent.setter
    def percent(self, percent):
        """Sets the percent of this Partner3DGeeksAlert.


        :param percent: The percent of this Partner3DGeeksAlert.  # noqa: E501
        :type percent: int
        """
        if self.local_vars_configuration.client_side_validation and percent is None:  # noqa: E501
            raise ValueError("Invalid value for `percent`, must not be `None`")  # noqa: E501

        self._percent = percent

    @property
    def image(self):
        """Gets the image of this Partner3DGeeksAlert.  # noqa: E501


        :return: The image of this Partner3DGeeksAlert.  # noqa: E501
        :rtype: str
        """
        return self._image

    @image.setter
    def image(self, image):
        """Sets the image of this Partner3DGeeksAlert.


        :param image: The image of this Partner3DGeeksAlert.  # noqa: E501
        :type image: str
        """

        self._image = image

    @property
    def action(self):
        """Gets the action of this Partner3DGeeksAlert.  # noqa: E501


        :return: The action of this Partner3DGeeksAlert.  # noqa: E501
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this Partner3DGeeksAlert.


        :param action: The action of this Partner3DGeeksAlert.  # noqa: E501
        :type action: str
        """
        if self.local_vars_configuration.client_side_validation and action is None:  # noqa: E501
            raise ValueError("Invalid value for `action`, must not be `None`")  # noqa: E501

        self._action = action

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Partner3DGeeksAlert):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Partner3DGeeksAlert):
            return True

        return self.to_dict() != other.to_dict()
