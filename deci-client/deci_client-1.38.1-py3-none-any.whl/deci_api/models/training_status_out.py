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


class TrainingStatusOut(object):
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
        'percentage': 'float',
        'created_at': 'datetime',
        'status': 'TaskStatus'
    }

    attribute_map = {
        'task_id': 'taskId',
        'percentage': 'percentage',
        'created_at': 'createdAt',
        'status': 'status'
    }

    def __init__(self, task_id=None, percentage=None, created_at=None, status=None, local_vars_configuration=None):  # noqa: E501
        """TrainingStatusOut - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._task_id = None
        self._percentage = None
        self._created_at = None
        self._status = None
        self.discriminator = None

        self.task_id = task_id
        self.percentage = percentage
        self.created_at = created_at
        self.status = status

    @property
    def task_id(self):
        """Gets the task_id of this TrainingStatusOut.  # noqa: E501


        :return: The task_id of this TrainingStatusOut.  # noqa: E501
        :rtype: str
        """
        return self._task_id

    @task_id.setter
    def task_id(self, task_id):
        """Sets the task_id of this TrainingStatusOut.


        :param task_id: The task_id of this TrainingStatusOut.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and task_id is None:  # noqa: E501
            raise ValueError("Invalid value for `task_id`, must not be `None`")  # noqa: E501

        self._task_id = task_id

    @property
    def percentage(self):
        """Gets the percentage of this TrainingStatusOut.  # noqa: E501


        :return: The percentage of this TrainingStatusOut.  # noqa: E501
        :rtype: float
        """
        return self._percentage

    @percentage.setter
    def percentage(self, percentage):
        """Sets the percentage of this TrainingStatusOut.


        :param percentage: The percentage of this TrainingStatusOut.  # noqa: E501
        :type: float
        """
        if self.local_vars_configuration.client_side_validation and percentage is None:  # noqa: E501
            raise ValueError("Invalid value for `percentage`, must not be `None`")  # noqa: E501

        self._percentage = percentage

    @property
    def created_at(self):
        """Gets the created_at of this TrainingStatusOut.  # noqa: E501


        :return: The created_at of this TrainingStatusOut.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this TrainingStatusOut.


        :param created_at: The created_at of this TrainingStatusOut.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def status(self):
        """Gets the status of this TrainingStatusOut.  # noqa: E501


        :return: The status of this TrainingStatusOut.  # noqa: E501
        :rtype: TaskStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this TrainingStatusOut.


        :param status: The status of this TrainingStatusOut.  # noqa: E501
        :type: TaskStatus
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

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
        if not isinstance(other, TrainingStatusOut):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, TrainingStatusOut):
            return True

        return self.to_dict() != other.to_dict()
