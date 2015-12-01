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
# Visit the Fedex Sandbox / Dev Resource Center to get your credentials.
# CONFIG_OBJ = FedexConfig(key='xxxxxxxxxxx',
#                          password='xxxxxxxxxxx',
#                          account_number='xxxxxxxxxxx',
#                          meter_number='xxxxxxxxxxx',
#                          freight_account_number='xxxxxxxxxxx',
#                          use_test_server=True)
#
# Fanx Test
# CONFIG_OBJ = FedexConfig(key='ASbmbcphSw8f1ZHd',
#                          password='h3OxgU9csCId9stQZQsnXyjL0',
#                          account_number='510087623',
#                          meter_number='118697731',
#                          freight_account_number='510087020',
#                          use_test_server=True)
#

# # fanx prod
CONFIG_OBJ = FedexConfig(key='jEJG8iz9PvknpK0o',
                         password='LFpsPRF4EupHc4TdifCN8DHV0',
                         account_number='451776185',
                         meter_number='5749788',
                         use_test_server=False)

