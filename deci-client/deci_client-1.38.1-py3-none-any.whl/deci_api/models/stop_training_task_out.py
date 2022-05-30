# coding: utf-8

"""
    Deci Platform API

    Train, deploy, optimize and serve your models using Deci's platform, In your cloud or on premise.  # noqa: E501

    The version of the OpenAPI document: 1.19.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from deci_client.deci_api.configuration import Configuration


class StopTrainingTaskOut(object):
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
        'task_id': 'str',
        'previous_status': 'TaskStatus',
        'current_status': 'TaskStatus'
    }

    attribute_map = {
        'task_id': 'taskId',
        'previous_status': 'previousStatus',
        'current_status': 'currentStatus'
    }

    def __init__(self, task_id=None, previous_status=None, current_status=None, local_vars_configuration=None):  # noqa: E501
        """StopTrainingTaskOut - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._task_id = None
        self._previous_status = None
        self._current_status = None
        self.discriminator = None

        self.task_id = task_id
        self.previous_status = previous_status
        self.current_status = current_status

    @property
    def task_id(self):
        """Gets the task_id of this StopTrainingTaskOut.  # noqa: E501


        :return: The task_id of this StopTrainingTaskOut.  # noqa: E501
        :rtype: str
        """
        return self._task_id

    @task_id.setter
    def task_id(self, task_id):
        """Sets the task_id of this StopTrainingTaskOut.


        :param task_id: The task_id of this StopTrainingTaskOut.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and task_id is None:  # noqa: E501
            raise ValueError("Invalid value for `task_id`, must not be `None`")  # noqa: E501

        self._task_id = task_id

    @property
    def previous_status(self):
        """Gets the previous_status of this StopTrainingTaskOut.  # noqa: E501


        :return: The previous_status of this StopTrainingTaskOut.  # noqa: E501
        :rtype: TaskStatus
        """
        return self._previous_status

    @previous_status.setter
    def previous_status(self, previous_status):
        """Sets the previous_status of this StopTrainingTaskOut.


        :param previous_status: The previous_status of this StopTrainingTaskOut.  # noqa: E501
        :type: TaskStatus
        """
        if self.local_vars_configuration.client_side_validation and previous_status is None:  # noqa: E501
            raise ValueError("Invalid value for `previous_status`, must not be `None`")  # noqa: E501

        self._previous_status = previous_status

    @property
    def current_status(self):
        """Gets the current_status of this StopTrainingTaskOut.  # noqa: E501


        :return: The current_status of this StopTrainingTaskOut.  # noqa: E501
        :rtype: TaskStatus
        """
        return self._current_status

    @current_status.setter
    def current_status(self, current_status):
        """Sets the current_status of this StopTrainingTaskOut.


        :param current_status: The current_status of this StopTrainingTaskOut.  # noqa: E501
        :type: TaskStatus
        """
        if self.local_vars_configuration.client_side_validation and current_status is None:  # noqa: E501
            raise ValueError("Invalid value for `current_status`, must not be `None`")  # noqa: E501

        self._current_status = current_status

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, StopTrainingTaskOut):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, StopTrainingTaskOut):
            return True

        return self.to_dict() != other.to_dict()
