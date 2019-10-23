"""
The L{config} module contains the L{FedexConfig} class, which is passed to
the Fedex API calls. It stores useful information such as your Web Services
account numbers and keys.

It is strongly suggested that you create a single L{FedexConfig} object in
your project and pass that to the various API calls, rather than create new
L{FedexConfig} objects haphazardly. This is merely a design suggestion,
treat it as such.
"""
import os


class FedexConfig(object):
    """
    Base configuration class that is used for the different Fedex SOAP calls.
    These are generally passed to the Fedex request classes as arguments.
    You may instantiate a L{FedexConfig} object with the minimal C{key} and
    C{password} arguments and set the instance variables documented below
    at a later time if you must.
    """

    def __init__(self, key, password, account_number=None, meter_number=None, freight_account_number=None,
                 integrator_id=None, wsdl_path=None, express_region_code=None, use_test_server=False, proxy=None):
        """
        @type key: L{str}
        @param key: Developer test key.
        @type password: L{str}
        @param password: The Fedex-generated password for your Web Systems
            account. This is generally emailed to you after registration.
        @type account_number: L{str}
        @keyword account_number: The account number sent to you by Fedex after
            registering for Web Services.
        @type meter_number: L{str}
        @keyword meter_number: The meter number sent to you by Fedex after
            registering for Web Services.
        @type freight_account_number: L{str}
        @keyword freight_account_number: The freight account number sent to you
            by Fedex after registering for Web Services.
        @type integrator_id: L{str}
        @keyword integrator_id: The integrator string sent to you by Fedex after
            registering for Web Services.
        @type wsdl_path: L{str}
        @keyword wsdl_path: In the event that you want to override the path to
            your WSDL directory, do so with this argument.
        @type use_test_server: L{bool}
        @keyword use_test_server: When this is True, test server WSDLs are used
            instead of the production server. You will also need to make sure
            that your L{FedexConfig} object has a production account number,
            meter number, authentication key, and password.
        @type proxy: L{str}
        @keyword proxy: Enter your list of proxy servers int the format 
            proxy = {'http': "http://......:8080", 'https': "http://.......:8080", }
            if needed.
        """
        self.key = key
        """@ivar: Developer test key."""
        self.password = password
        """@ivar: Fedex Web Services password."""
        self.account_number = account_number
        """@ivar: Web Services account number."""
        self.meter_number = meter_number
        """@ivar: Web services meter number."""
        self.freight_account_number = freight_account_number
        """@ivar: Web Services freight accountnumber."""
        self.integrator_id = integrator_id
        """@ivar: Web services integrator ID."""
        self.express_region_code = express_region_code
        """@ivar: Web services ExpressRegionCode"""
        self.use_test_server = use_test_server
        """@ivar: When True, point to the test server."""
        self.proxy = proxy
        """@ivar: A list of proxy servers."""

        # Allow overriding of the WDSL path.
        if wsdl_path is None:
            self.wsdl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          'wsdl')
        else:  # pragma: no cover
            self.wsdl_path = wsdl_path
