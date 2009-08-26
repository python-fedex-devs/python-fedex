import os
import sys

class FedexConfig(object):
    """
    Base configuration class that is used for the different Fedex SOAP calls.
    """
    def __init__(self, key, password, account_number=None, meter_number=None,
                 integrator_id=None, wsdl_path=None):
        self.key = key
        self.password = password
        self.account_number = account_number
        self.meter_number = meter_number
        self.integrator_id = integrator_id
        
        # Allow overriding of the WDSL path.
        if wsdl_path == None:
            self.wsdl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                          'wsdl')
        else:
            self.wsdl_path = wsdl_path