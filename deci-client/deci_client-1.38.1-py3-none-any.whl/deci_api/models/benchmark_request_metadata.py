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


class BenchmarkRequestMetadata(object):
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
        'update_time': 'datetime',
        'creation_time': 'datetime',
        'request_id': 'str',
        'model_id': 'str',
        'status': 'BenchmarkRequestStatus',
        'results': 'list[ModelBenchmarkResultsMetadata]'
    }

    attribute_map = {
        'update_time': 'updateTime',
        'creation_time': 'creationTime',
        'request_id': 'requestId',
        'model_id': 'modelId',
        'status': 'status',
        'results': 'results'
    }

    def __init__(self, update_time=None, creation_time=None, request_id=None, model_id=None, status=None, results=[], local_vars_configuration=None):  # noqa: E501
        """BenchmarkRequestMetadata - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._update_time = None
        self._creation_time = None
        self._request_id = None
        self._model_id = None
        self._status = None
        self._results = None
        self.discriminator = None

        if update_time is not None:
            self.update_time = update_time
        if creation_time is not None:
            self.creation_time = creation_time
        self.request_id = request_id
        self.model_id = model_id
        if status is not None:
            self.status = status
        if results is not None:
            self.results = results

    @property
    def update_time(self):
        """Gets the update_time of this BenchmarkRequestMetadata.  # noqa: E501


        :return: The update_time of this BenchmarkRequestMetadata.  # noqa: E501
        :rtype: datetime
        """
        return self._update_time

    @update_time.setter
    def update_time(self, update_time):
        """Sets the update_time of this BenchmarkRequestMetadata.


        :param update_time: The update_time of this BenchmarkRequestMetadata.  # noqa: E501
        :type: datetime
        """

        self._update_time = update_time

    @property
    def creation_time(self):
        """Gets the creation_time of this BenchmarkRequestMetadata.  # noqa: E501


        :return: The creation_time of this BenchmarkRequestMetadata.  # noqa: E501
        :rtype: datetime
        """
        return self._creation_time

    @creation_time.setter
    def creation_time(self, creation_time):
        """Sets the creation_time of this BenchmarkRequestMetadata.


        :param creation_time: The creation_time of this BenchmarkRequestMetadata.  # noqa: E501
        :type: datetime
        """

        self._creation_time = creation_time

    @property
    def request_id(self):
        """Gets the request_id of this BenchmarkRequestMetadata.  # noqa: E501


        :return: The request_id of this BenchmarkRequestMetadata.  # noqa: E501
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """Sets the request_id of this BenchmarkRequestMetadata.


        :param request_id: The request_id of this BenchmarkRequestMetadata.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and request_id is None:  # noqa: E501
            raise ValueError("Invalid value for `request_id`, must not be `None`")  # noqa: E501

        self._request_id = request_id

    @property
    def model_id(self):
        """Gets the model_id of this BenchmarkRequestMetadata.  # noqa: E501


        :return: The model_id of this BenchmarkRequestMetadata.  # noqa: E501
        :rtype: str
        """
        return self._model_id

    @model_id.setter
    def model_id(self, model_id):
        """Sets the model_id of this BenchmarkRequestMetadata.


        :param model_id: The model_id of this BenchmarkRequestMetadata.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and model_id is None:  # noqa: E501
            raise ValueError("Invalid value for `model_id`, must not be `None`")  # noqa: E501

        self._model_id = model_id

    @property
    def status(self):
        """Gets the status of this BenchmarkRequestMetadata.  # noqa: E501


        :return: The status of this BenchmarkRequestMetadata.  # noqa: E501
        :rtype: BenchmarkRequestStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this BenchmarkRequestMetadata.


        :param status: The status of this BenchmarkRequestMetadata.  # noqa: E501
        :type: BenchmarkRequestStatus
        """

        self._status = status

    @property
    def results(self):
        """Gets the results of this BenchmarkRequestMetadata.  # noqa: E501


        :return: The results of this BenchmarkRequestMetadata.  # noqa: E501
        :rtype: list[ModelBenchmarkResultsMetadata]
        """
        return self._results

    @results.setter
    def results(self, results):
        """Sets the results of this BenchmarkRequestMetadata.


        :param results: The results of this BenchmarkRequestMetadata.  # noqa: E501
        :type: list[ModelBenchmarkResultsMetadata]
        """

        self._results = results

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
        if not isinstance(other, BenchmarkRequestMetadata):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BenchmarkRequestMetadata):
            return True

        return self.to_dict() != other.to_dict()
