"""
This file holds configuration for your test account. Make SURE to change
the values below to your account's TESTING meter number.
"""
import os
import sys
# Use the fedex directory included in the downloaded package instead of
# any globally installed versions.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fedex.config import FedexConfig

CONFIG_OBJ = FedexConfig(key='ZyNQQFdcxUATOx9L',
                         password='8irpTkULT1zjVLlL8XiVczTex',
                         account_number='510087780',
                         meter_number='118501898',
                         use_test_server=True)