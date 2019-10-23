from fedex.base_service import FedexBaseService


class FedexCreatePickupRequest(FedexBaseService):

    def __init__(self, config_obj, *args, **kwargs):
        self._config_obj = config_obj
        # Holds version info for the VersionId SOAP object.
        self._version_info = {
            'service_id': 'disp',
            'major': '17',
            'intermediate': '0',
            'minor': '0'
        }
        self.OriginDetail = None
        self.PackageCount = None
        self.TotalWeight = None
        self.CarrierCode = None
        self.OversizePackageCount = None
        self.Remarks = None
        self.CommodityDescription = None
        self.CountryRelationship = None
        self.PickupServiceCategory = None
        super(FedexCreatePickupRequest, self).__init__(self._config_obj, 'PickupService_v17.wsdl', *args, **kwargs)

    def _prepare_wsdl_objects(self):
        self.OriginDetail = self.client.factory.create('PickupOriginDetail')

        self.OriginDetail.PickupLocation = self.client.factory.create('ContactAndAddress')
        self.OriginDetail.PickupLocation.Contact = self.client.factory.create('Contact')
        self.OriginDetail.PickupLocation.Address = self.client.factory.create('Address')
        self.OriginDetail.PackageLocation = None
        self.OriginDetail.BuildingPart = None

        self.TotalWeight = self.client.factory.create('Weight')

        self.CarrierCode = self.client.factory.create('CarrierCodeType')

        self.logger.debug(self.OriginDetail)
        self.logger.debug(self.TotalWeight)
        self.logger.debug(self.CarrierCode)

    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.

        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(),
            WHICH RESIDES ON FedexBaseService AND IS INHERITED.
        """

        # Fire off the query.
        return self.client.service.createPickup(
            WebAuthenticationDetail=self.WebAuthenticationDetail,
            ClientDetail=self.ClientDetail,
            TransactionDetail=self.TransactionDetail,
            Version=self.VersionId,
            OriginDetail=self.OriginDetail,
            PickupServiceCategory=self.PickupServiceCategory,
            PackageCount=self.PackageCount,
            TotalWeight=self.TotalWeight,
            CarrierCode=self.CarrierCode,
            OversizePackageCount=self.OversizePackageCount,
            Remarks=self.Remarks,
            CommodityDescription=self.CommodityDescription,
            CountryRelationship=self.CountryRelationship
        )


class FedexPickupAvailabilityRequest(FedexBaseService):

    def __init__(self, config_obj, *args, **kwargs):
        self._config_obj = config_obj
        # Holds version info for the VersionId SOAP object.
        self._version_info = {
            'service_id': 'disp',
            'major': '17',
            'intermediate': '0',
            'minor': '0'
        }
        self.PickupType = None
        self.AccountNumber = None
        self.PickupAddress = None
        self.PickupRequestType = None
        self.DispatchDate = None
        self.NumberOfBusinessDays = None
        self.PackageReadyTime = None
        self.CustomerCloseTime = None
        self.Carriers = None
        self.ShipmentAttributes = None
        self.PackageDetails = None
        super(FedexPickupAvailabilityRequest, self).__init__(self._config_obj, 'PickupService_v17.wsdl', *args, **kwargs)

    def _prepare_wsdl_objects(self):
        self.Carriers = 'FDXE'

        self.AccountNumber = self.client.factory.create('AssociatedAccount')
        self.AccountNumber.Type = None
        self.AccountNumber.AccountNumber = None

        self.PickupAddress = self.client.factory.create('Address')

        self.ShipmentAttributes = self.client.factory.create('PickupShipmentAttributes')
        self.ShipmentAttributes.ServiceType = None
        self.ShipmentAttributes.PackagingType = None

        self.ShipmentAttributes.Dimensions = self.client.factory.create('Dimensions')
        self.ShipmentAttributes.Dimensions.Length = None
        self.ShipmentAttributes.Dimensions.Width = None
        self.ShipmentAttributes.Dimensions.Height = None
        self.ShipmentAttributes.Dimensions.Units = None

        self.ShipmentAttributes.Weight = self.client.factory.create('Weight')
        self.ShipmentAttributes.Weight.Units = None
        self.ShipmentAttributes.Weight.Value = None

        self.PackageDetails = self.client.factory.create('RequestedPickupPackageDetail')
        self.PackageDetails.PackageSpecialServices = self.client.factory.create('PickupPackageSpecialServicesRequested')
        self.PackageDetails.Weight = self.client.factory.create('Weight')

    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.

        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(),
            WHICH RESIDES ON FedexBaseService AND IS INHERITED.
        """

        # Fire off the query.
        return self.client.service.getPickupAvailability(
            WebAuthenticationDetail=self.WebAuthenticationDetail,
            ClientDetail=self.ClientDetail,
            TransactionDetail=self.TransactionDetail,
            Version=self.VersionId,
            PickupType=self.PickupType,
            AccountNumber=self.AccountNumber,
            PickupAddress=self.PickupAddress,
            PickupRequestType=self.PickupRequestType,
            DispatchDate=self.DispatchDate,
            NumberOfBusinessDays=self.NumberOfBusinessDays,
            PackageReadyTime=self.PackageReadyTime,
            CustomerCloseTime=self.CustomerCloseTime,
            Carriers=self.Carriers,
            ShipmentAttributes=self.ShipmentAttributes,
            PackageDetails=self.PackageDetails
        )

class FedexCancelPickupRequest(FedexBaseService):
    """
    This class allows you to cancel a pickup request, given a dispatch confirmation number.
    """

    def __init__(self, config_obj, *args, **kwargs):
        """
        Cancels a pickup request via a dispatch confirmation number.
        """

        self._config_obj = config_obj

        # Holds version info for the VersionId SOAP object.
        self._version_info = {'service_id': 'disp', 'major': '17',
                              'intermediate': '0', 'minor': '0'}
        self.CarrierCode = None
        self.PickupConfirmationNumber = None
        self.ScheduledDate = None
        self.EndDate = None
        self.Location = None
        self.Remarks = None
        self.ShippingChargesPayment = None
        self.Reason = None
        self.ContactName = None
        self.PhoneNumber = None
        self.PhoneExtension = None
        # Call the parent FedexBaseService class for basic setup work.
        super(FedexCancelPickupRequest, self).__init__(self._config_obj,
                                                         'PickupService_v17.wsdl',
                                                         *args, **kwargs)

    def _prepare_wsdl_objects(self):
        """
        Preps the WSDL data structures for the user.
        """

        self.CarrierCode = self.client.factory.create('CarrierCodeType')
        self.ShippingChargesPayment = self.client.factory.create('Payment')

    def _assemble_and_send_request(self):
        """
        Fires off the Fedex request.
        
        @warning: NEVER CALL THIS METHOD DIRECTLY. CALL send_request(), WHICH RESIDES
            ON FedexBaseService AND IS INHERITED.
        """

        # Fire off the query.
        return self.client.service.cancelPickup(
            WebAuthenticationDetail=self.WebAuthenticationDetail,
            ClientDetail=self.ClientDetail,
            TransactionDetail=self.TransactionDetail,
            Version=self.VersionId,
            CarrierCode=self.CarrierCode,
            PickupConfirmationNumber=self.PickupConfirmationNumber,
            ScheduledDate=self.ScheduledDate,
            EndDate=self.EndDate,
            Location=self.Location,
            Remarks=self.Remarks,
            ShippingChargesPayment=self.ShippingChargesPayment,
            Reason=self.Reason,
            ContactName=self.ContactName,
            PhoneNumber=self.PhoneNumber,
            PhoneExtension=self.PhoneExtension
        )

