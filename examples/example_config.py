"""
This file holds various configuration options used for all of the examples.

You will need to change the values below to match your test account.
"""
import os
import sys
# Use the fedex directory included in the downloaded package instead of
# any globally installed versions.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fedex.config import FedexConfig

# Change these values to match your testing account/meter number.
CONFIG_OBJ = FedexConfig(key='xxxxxxxxxxxxxxxx',
                         password='xxxxxxxxxxxxxxxxxxxxxxxxx',
                         account_number='#########',
                         meter_number='#########',
                         use_test_server=True)