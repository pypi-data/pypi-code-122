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


class AccuracyMetricKey(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    allowed enum values
    """
    TOP_1 = "Top-1"
    TOP_5 = "Top-5"
    AUC = "AUC"
    PRECISION = "Precision"
    RECALL = "Recall"
    F1_SCORE = "F1 Score"
    TRUE_POSITIVES = "True Positives"
    TRUE_NEGATIVES = "True Negatives"
    FALSE_POSITIVES = "False Positives"
    FALSE_NEGATIVES = "False Negatives"
    MIOU = "mIoU"
    PIXEL_ACCURACY = "Pixel Accuracy"
    DICE_COEFFICIENT_F1_SCORE_ = "Dice Coefficient (F1 Score)"
    MAP = "mAP"
    MAP_0_5_0_95 = "mAP@0.5:0.95"
    D1 = "D1"
    D2 = "D2"
    D3 = "D3"
    ABSREL = "AbsRel"
    SQREL = "SqRel"
    ROOT_MEAN_SQUARED_ERROR = "Root Mean Squared Error"
    ROOT_MEAN_SQUARED_ERROR_LOG = "Root Mean Squared Error - Log"
    SLLOG = "Sllog"
    LOG_10 = "Log-10"
    PCK = "PCK"
    PCKH = "PCKh"
    PDJ = "PDJ"
    OKS = "OKS"
    CUSTOM = "Custom"

    allowable_values = [TOP_1, TOP_5, AUC, PRECISION, RECALL, F1_SCORE, TRUE_POSITIVES, TRUE_NEGATIVES, FALSE_POSITIVES, FALSE_NEGATIVES, MIOU, PIXEL_ACCURACY, DICE_COEFFICIENT_F1_SCORE_, MAP, MAP_0_5_0_95, D1, D2, D3, ABSREL, SQREL, ROOT_MEAN_SQUARED_ERROR, ROOT_MEAN_SQUARED_ERROR_LOG, SLLOG, LOG_10, PCK, PCKH, PDJ, OKS, CUSTOM]  # noqa: E501

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
    }

    attribute_map = {
    }

    def __init__(self, local_vars_configuration=None):  # noqa: E501
        """AccuracyMetricKey - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration
        self.discriminator = None

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
        if not isinstance(other, AccuracyMetricKey):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AccuracyMetricKey):
            return True

        return self.to_dict() != other.to_dict()
