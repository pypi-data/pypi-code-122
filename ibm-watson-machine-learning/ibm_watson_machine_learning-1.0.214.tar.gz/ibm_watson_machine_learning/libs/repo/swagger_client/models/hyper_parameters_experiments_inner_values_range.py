# coding: utf-8

"""

    No descripton provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

#  (C) Copyright IBM Corp. 2021.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from pprint import pformat
from six import iteritems
import re


class HyperParametersExperimentsInnerValuesRange(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, _from=None, to=None, step=None):
        """
        HyperParametersExperimentsInnerValuesRange - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            '_from': 'float',
            'to': 'float',
            'step': 'float'
        }

        self.attribute_map = {
            '_from': 'from',
            'to': 'to',
            'step': 'step'
        }

        self.__from = _from
        self._to = to
        self._step = step

    @property
    def _from(self):
        """
        Gets the _from of this HyperParametersExperimentsInnerValuesRange.


        :return: The _from of this HyperParametersExperimentsInnerValuesRange.
        :rtype: float
        """
        return self.__from

    @_from.setter
    def _from(self, _from):
        """
        Sets the _from of this HyperParametersExperimentsInnerValuesRange.


        :param _from: The _from of this HyperParametersExperimentsInnerValuesRange.
        :type: float
        """

        self.__from = _from

    @property
    def to(self):
        """
        Gets the to of this HyperParametersExperimentsInnerValuesRange.


        :return: The to of this HyperParametersExperimentsInnerValuesRange.
        :rtype: float
        """
        return self._to

    @to.setter
    def to(self, to):
        """
        Sets the to of this HyperParametersExperimentsInnerValuesRange.


        :param to: The to of this HyperParametersExperimentsInnerValuesRange.
        :type: float
        """

        self._to = to

    @property
    def step(self):
        """
        Gets the step of this HyperParametersExperimentsInnerValuesRange.


        :return: The step of this HyperParametersExperimentsInnerValuesRange.
        :rtype: float
        """
        return self._step

    @step.setter
    def step(self, step):
        """
        Sets the step of this HyperParametersExperimentsInnerValuesRange.


        :param step: The step of this HyperParametersExperimentsInnerValuesRange.
        :type: float
        """

        self._step = step

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
