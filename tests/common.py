"""
This module contains common definitions and functions used within the
test suite.
"""
from fedex.config import FedexConfig


def get_fedex_config():
    """
    Returns a basic FedexConfig to test with.
    """
    # Test server (Enter your credentials here)
    return FedexConfig(key='',
                         password='',
                         account_number='',
                         meter_number='',
                         use_test_server=True,
                         proxy = None)
