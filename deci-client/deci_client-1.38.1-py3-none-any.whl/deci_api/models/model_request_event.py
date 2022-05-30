# coding: utf-8

"""
    Deci Platform API

    Train, deploy, optimize and serve your models using Deci's platform, In your cloud or on premise.  # noqa: E501

    The version of the OpenAPI document: 4.0.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from deci_client.deci_api.configuration import Configuration


class ModelRequestEvent(object):
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
        'task': 'DeepLearningTask',
        'hardware': 'HardwareType',
        'batch_size': 'AnyOfBatchSizeEdgeBatchSize',
        'kpis': 'list[KPI]'
    }

    attribute_map = {
        'task': 'task',
        'hardware': 'hardware',
        'batch_size': 'batchSize',
        'kpis': 'kpis'
    }

    def __init__(self, task=None, hardware=None, batch_size=None, kpis=None, local_vars_configuration=None):  # noqa: E501
        """ModelRequestEvent - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._task = None
        self._hardware = None
        self._batch_size = None
        self._kpis = None
        self.discriminator = None

        self.task = task
        self.hardware = hardware
        if batch_size is not None:
            self.batch_size = batch_size
        if kpis is not None:
            self.kpis = kpis

    @property
    def task(self):
        """Gets the task of this ModelRequestEvent.  # noqa: E501


        :return: The task of this ModelRequestEvent.  # noqa: E501
        :rtype: DeepLearningTask
        """
        return self._task

    @task.setter
    def task(self, task):
        """Sets the task of this ModelRequestEvent.


        :param task: The task of this ModelRequestEvent.  # noqa: E501
        :type: DeepLearningTask
        """
        if self.local_vars_configuration.client_side_validation and task is None:  # noqa: E501
            raise ValueError("Invalid value for `task`, must not be `None`")  # noqa: E501

        self._task = task

    @property
    def hardware(self):
        """Gets the hardware of this ModelRequestEvent.  # noqa: E501


        :return: The hardware of this ModelRequestEvent.  # noqa: E501
        :rtype: HardwareType
        """
        return self._hardware

    @hardware.setter
    def hardware(self, hardware):
        """Sets the hardware of this ModelRequestEvent.


        :param hardware: The hardware of this ModelRequestEvent.  # noqa: E501
        :type: HardwareType
        """
        if self.local_vars_configuration.client_side_validation and hardware is None:  # noqa: E501
            raise ValueError("Invalid value for `hardware`, must not be `None`")  # noqa: E501

        self._hardware = hardware

    @property
    def batch_size(self):
        """Gets the batch_size of this ModelRequestEvent.  # noqa: E501


        :return: The batch_size of this ModelRequestEvent.  # noqa: E501
        :rtype: AnyOfBatchSizeEdgeBatchSize
        """
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size):
        """Sets the batch_size of this ModelRequestEvent.


        :param batch_size: The batch_size of this ModelRequestEvent.  # noqa: E501
        :type: AnyOfBatchSizeEdgeBatchSize
        """

        self._batch_size = batch_size

    @property
    def kpis(self):
        """Gets the kpis of this ModelRequestEvent.  # noqa: E501


        :return: The kpis of this ModelRequestEvent.  # noqa: E501
        :rtype: list[KPI]
        """
        return self._kpis

    @kpis.setter
    def kpis(self, kpis):
        """Sets the kpis of this ModelRequestEvent.


        :param kpis: The kpis of this ModelRequestEvent.  # noqa: E501
        :type: list[KPI]
        """

        self._kpis = kpis

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
        if not isinstance(other, ModelRequestEvent):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ModelRequestEvent):
            return True

        return self.to_dict() != other.to_dict()
