# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# © Copyright IBM Corp. 2021, 2022  All Rights Reserved.
# US Government Users Restricted Rights -Use, duplication or disclosure restricted by 
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------
from abc import abstractmethod

from ibm_metrics_plugin.metrics.explainability.entity.explain_config import ExplainConfig


class BaseExplainer():

    def __init__(self, explain_config: ExplainConfig):
        self.config = explain_config

    @abstractmethod
    def is_supported(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def explain_data(self, data, **kwargs):
        pass

    @abstractmethod
    def get_data_to_accumulate(self, response):
        pass

    def explain(self, data, **kwargs):
        self.initialize()
        return self.explain_data(data=data, **kwargs)
