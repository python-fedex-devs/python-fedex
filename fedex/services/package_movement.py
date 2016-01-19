"""
Package Movement Information Service

This package contains classes to check service availability, route, and postal
codes. Defined by the PackageMovementInformationService WSDL file. 
"""
import warnings

from ..base_service import FedexBaseService, FedexError


class FedexPostalCodeNotFound(FedexError):
    """
    Exception: Sent when the postalcode is missing.
    """
    pass


class FedexInvalidPostalCodeFormat(FedexError):
    """
    Exception: Sent when the postal code is invalid
    """
    pass


class PostalCodeInquiryRequest(FedexBaseService):
    """
    The postal code inquiry enables customers to validate postal codes
    and service commitments.
    """

    def __init__(self, config_obj, postal_code=None, country_code=None, *args, **kwargs):
        """
        Sets up an inquiry request. The optional keyword args
        detailed on L{FedexBaseService} apply here as well.
        
        @type config_obj: L{FedexConfig}
        @param config_obj: A valid FedexConfig object
        @param postal_code: a valid postal code
        @param country_code: ISO country code to which the postal code belongs to.
        """
        self._config_obj = config_obj

        # Holds version info for the VersionId SOAP object.
        self._version_info = {'service_id': 'pmis',
                              'major': '4',
                              'intermediate': '0',
                              'minor': '0'}

        self.PostalCode = postal_code
        self.CountryCode = country_code

        warnings.warn(
                "Package Movement Service has been deprecated; "
                "please use Country Service for postal code validation requests or "
                "Availability and Commitment Service for service availability "
                "requests instead.",
                DeprecationWarning
        )

        # Call the parent FedexBaseService class for basic setup work.
        super(PostalCodeInquiryRequest, self).__init__(self._config_obj,
                                                       'PackageMovementInformationService_v4.wsdl',
                                                       *args, **kwargs)

    def _check_response_for_request_errors(self):
        """
        Checks the response to see if there were any errors specific to
        this WSDL.
        """
        if self.response.HighestSeverity == "ERROR":
            for notification in self.response.Notifications:  # pragma: no cover
                if notification.Severity == "ERROR":
                    if "Postal Code Not Found" in notification.Message:
                        raise FedexPostalCodeNotFound(notification.Code,
                                                      notification.Message)

                    elif "Invalid Postal Code Format" in self.response.Notifications:
                        raise FedexInvalidPostalCodeFormat(notification.Code,
                                                           notification.Message)
                    else:
                        raise FedexError(notification.Code,
                                         notification.Message)

    def _prepare_wsdl_objects(self):
        """
        Preps the WSDL data structures for the user.
        """

        self.CarrierCode = 'FDXE'

    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.
        
        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(), WHICH RESIDES
            ON FedexBaseService AND IS INHERITED.
        """

        client = self.client

        # We get an exception like this when specifying an IntegratorId:
        # suds.TypeNotFound: Type not found: 'IntegratorId'
        # Setting it to None does not seem to appease it.

        del self.ClientDetail.IntegratorId

        # Fire off the query.
        response = client.service.postalCodeInquiry(WebAuthenticationDetail=self.WebAuthenticationDetail,
                                                    ClientDetail=self.ClientDetail,
                                                    TransactionDetail=self.TransactionDetail,
                                                    Version=self.VersionId,
                                                    PostalCode=self.PostalCode,
                                                    CountryCode=self.CountryCode,
                                                    CarrierCode=self.CarrierCode)

        return response
