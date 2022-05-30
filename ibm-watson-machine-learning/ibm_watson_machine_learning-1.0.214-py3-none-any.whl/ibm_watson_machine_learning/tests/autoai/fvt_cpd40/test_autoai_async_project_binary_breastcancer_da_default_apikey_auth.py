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

import unittest

import ibm_boto3
from ibm_watson_machine_learning import APIClient
from ibm_watson_machine_learning.helpers.connections import DataConnection, S3Location
from ibm_watson_machine_learning.utils.autoai.errors import WMLClientError
from ibm_watson_machine_learning.tests.utils import bucket_exists, create_bucket, is_cp4d
from ibm_watson_machine_learning.tests.autoai.abstract_tests_classes import AbstractTestAutoAIAsync, \
    AbstractTestWebservice

from ibm_watson_machine_learning.tests.utils import get_wml_credentials, is_cp4d

from ibm_watson_machine_learning.utils.autoai.enums import PredictionType, Metrics, ClassificationAlgorithms


@unittest.skipIf(not is_cp4d(), "Not supported on cloud")
class TestAutoAIRemote(AbstractTestAutoAIAsync, unittest.TestCase):
    """
    The test can be run on CPD only
    """

    cos_resource = None
    data_location = './autoai/data/breast_cancer.csv'

    data_cos_path = 'data/breast_cancer.csv'

    SPACE_ONLY = False

    OPTIMIZER_NAME = "breast_cancer test sdk"

    target_space_id = None

    experiment_info = dict(
        name=OPTIMIZER_NAME,
        prediction_type=PredictionType.BINARY,
        prediction_column='diagnosis',
        positive_label='M',
        scoring=Metrics.AVERAGE_PRECISION_SCORE,
        max_number_of_estimators=1,
        include_only_estimators=[ClassificationAlgorithms.LR]

    )

    @classmethod
    def setUpClass(cls) -> None:
        """
        Load WML credentials from config.ini file based on ENV variable.
        """
        cls.wml_credentials = get_wml_credentials()
        try:
            del cls.wml_credentials['password']
        except:
            pass
        try:
            del cls.wml_credentials['bedrock_url']
        except:
            pass

        assert(cls.wml_credentials.get('username') is not None)
        assert(cls.wml_credentials.get('password') is None)
        assert (cls.wml_credentials.get('bedrock_url') is None)
        assert(cls.wml_credentials.get('apikey') is not None)
        cls.wml_client = APIClient(wml_credentials=cls.wml_credentials)

        cls.project_id = cls.wml_credentials.get('project_id')

    def test_00d_prepare_data_asset(self):
        asset_details = self.wml_client.data_assets.create(
            name=self.data_location.split('/')[-1],
            file_path=self.data_location)

        TestAutoAIRemote.asset_id = self.wml_client.data_assets.get_id(asset_details)
        self.assertIsInstance(self.asset_id, str)

    def test_02_data_reference_setup(self):
        TestAutoAIRemote.data_connection = DataConnection(data_asset_id=self.asset_id)
        TestAutoAIRemote.results_connection = None

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connection)
        self.assertIsNone(obj=TestAutoAIRemote.results_connection)

    def test_99_delete_data_asset(self):
        self.wml_client.data_assets.delete(self.asset_id)

        with self.assertRaises(WMLClientError):
            self.wml_client.data_assets.get_details(self.asset_id)


if __name__ == '__main__':
    unittest.main()
