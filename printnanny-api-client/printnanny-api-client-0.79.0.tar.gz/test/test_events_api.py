# coding: utf-8

"""
    printnanny-api-client

    Official API client library forprintnanny.ai print-nanny.com  # noqa: E501

    The version of the OpenAPI document: 0.0.0
    Contact: leigh@printnanny.ai
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import printnanny_api_client
from printnanny_api_client.api.events_api import EventsApi  # noqa: E501
from printnanny_api_client.rest import ApiException


class TestEventsApi(unittest.TestCase):
    """EventsApi unit test stubs"""

    def setUp(self):
        self.api = printnanny_api_client.api.events_api.EventsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_commands_create(self):
        """Test case for commands_create

        """
        pass

    def test_commands_list(self):
        """Test case for commands_list

        """
        pass

    def test_commands_retrieve(self):
        """Test case for commands_retrieve

        """
        pass

    def test_events_create(self):
        """Test case for events_create

        """
        pass

    def test_events_list(self):
        """Test case for events_list

        """
        pass

    def test_events_retrieve(self):
        """Test case for events_retrieve

        """
        pass


if __name__ == '__main__':
    unittest.main()
