"""
Test module for the Fedex Tools.
"""

import unittest
import logging
import sys

sys.path.insert(0, '..')

import fedex.config
import fedex.services.ship_service as service  # Any request object will do.
import fedex.tools.conversion

logging.getLogger('suds').setLevel(logging.ERROR)
logging.getLogger('fedex').setLevel(logging.INFO)


class FedexToolsTests(unittest.TestCase):
    """
    These tests verify that the fedex tools are working properly.
    """

    def test_conversion_tools(self):
        # Empty config, since we are not actually sending anything
        config = fedex.config.FedexConfig(key='', password='',
                                          account_number='', meter_number='',
                                          use_test_server=True)

        # We need a mock suds object, a request object or sub-object will do.
        waybill_request = service.FedexProcessShipmentRequest(config)
        obj = waybill_request.create_wsdl_object_of_type('ProcessShipmentRequest')

        # Test basic sobject to dict.
        dict_obj = fedex.tools.conversion.basic_sobject_to_dict(obj)
        assert type(dict_obj) == dict

        # Test with serialization and case conversion.
        dict_obj = fedex.tools.conversion.sobject_to_dict(obj, key_to_lower=True, json_serialize=True)
        assert type(dict_obj) == dict

        # JSON string object test
        dict_obj = fedex.tools.conversion.sobject_to_json(obj)
        assert dict_obj, "Expecting a JSON string object."


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    unittest.main()
