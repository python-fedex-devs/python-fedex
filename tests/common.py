"""
This module contains common definitions and functions used within the
test suite.
"""
from fedex.config import FedexConfig

def get_test_config():
    """
    Returns a basic FedexConfig to test with.
    """
    # Test server (Enter your credentials here)
    return FedexConfig(key='xxxxxxxxxxxxxxxxx',
                       password='xxxxxxxxxxxxxxxxxxxxxxxxx',
                       account_number='xxxxxxxxx',
                       meter_number='xxxxxxxxxx',
                       use_test_server=True)