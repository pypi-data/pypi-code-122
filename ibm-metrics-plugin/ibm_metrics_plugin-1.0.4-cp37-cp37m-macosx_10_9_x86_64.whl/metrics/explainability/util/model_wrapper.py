# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# © Copyright IBM Corp. 2021, 2022  All Rights Reserved.
# US Government Users Restricted Rights -Use, duplication or disclosure restricted by 
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------


class ModelWrapper():
    """
        Model Wrapper class to wrap user provided details related to black box model
    """
    def __init__(self, score_fn, **kwargs):
        self.score_fn = score_fn

        #Place holder values
        self.feature_columns = kwargs.get("feature_columns")
        self.meta_fields = kwargs.get("meta_fields")


    def score(self,df):
        """ 
            Wrapper to user provided score function
        """
        predictions, probabilities = self.score_fn(df)
        return probabilities, predictions