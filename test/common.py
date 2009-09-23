"""
This module contains common definitions and functions used within the
test suite.
"""
from fedex.config import FedexConfig

def get_test_config():
    """
    Returns a basic FedexConfig to test with.
    """
    """
    # Production server
    return FedexConfig(key='xxxxxxxxxxxxxxxxx',
                       password='xxxxxxxxxxxxxxxxxxxxxxxxx',
                       account_number='xxxxxxxxx',
                       meter_number='xxxxxxxxxx')
    """
    # Test server
    return FedexConfig(key='ZyNQQFdcxUATOx9L',
                       password='GtngmKzs4Dk4RYmrlAjrLykwi',
                       account_number='510087780',
                       meter_number='118501898',
                       use_test_server=True)