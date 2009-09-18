"""
This file holds various configuration options used for all of the examples.
"""
import os
import sys
# Use the fedex directory included in the downloaded package instead of
# any globally installed versions.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fedex.config import FedexConfig

CONFIG_OBJ = FedexConfig(key='ZyNQQFdcxUATOx9L',
                         password='GtngmKzs4Dk4RYmrlAjrLykwi',
                         account_number='510087780',
                         meter_number='118501898',
                         use_test_server=True)