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
import datetime

import printnanny_api_client
from printnanny_api_client.models.octo_printer_profile_request import OctoPrinterProfileRequest  # noqa: E501
from printnanny_api_client.rest import ApiException

class TestOctoPrinterProfileRequest(unittest.TestCase):
    """OctoPrinterProfileRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test OctoPrinterProfileRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = printnanny_api_client.models.octo_printer_profile_request.OctoPrinterProfileRequest()  # noqa: E501
        if include_optional :
            return OctoPrinterProfileRequest(
                axes_e_inverted = True, 
                axes_e_speed = -2147483648, 
                axes_x_speed = -2147483648, 
                axes_x_inverted = True, 
                axes_y_inverted = True, 
                axes_y_speed = -2147483648, 
                axes_z_inverted = True, 
                axes_z_speed = -2147483648, 
                extruder_count = -2147483648, 
                extruder_nozzle_diameter = 1.337, 
                extruder_shared_nozzle = True, 
                heated_bed = True, 
                heated_chamber = True, 
                model = '', 
                name = '0', 
                octoprint_key = '0', 
                volume_custom_box = {
                    'key' : null
                    }, 
                volume_depth = 1.337, 
                volume_formfactor = '0', 
                volume_height = 1.337, 
                volume_origin = '0', 
                volume_width = 1.337
            )
        else :
            return OctoPrinterProfileRequest(
                name = '0',
                octoprint_key = '0',
        )

    def testOctoPrinterProfileRequest(self):
        """Test OctoPrinterProfileRequest"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
