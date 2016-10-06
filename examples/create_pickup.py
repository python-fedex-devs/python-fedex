#!/usr/bin/env python
"""
This example shows how to create a pickup request
"""
import datetime

from example_config import CONFIG_OBJ
from fedex.services.pickup_service import FedexCreatePickupRequest

customer_transaction_id = "*** PickupService Request v11 using Python ***"  # Optional transaction_id
pickup_service = FedexCreatePickupRequest(CONFIG_OBJ, customer_transaction_id)

pickup_service.OriginDetail.PickupLocation.Contact.PersonName = 'Sender Name'
pickup_service.OriginDetail.PickupLocation.Contact.EMailAddress = 'test@user.com'
pickup_service.OriginDetail.PickupLocation.Contact.CompanyName = 'Acme Inc.'
pickup_service.OriginDetail.PickupLocation.Contact.PhoneNumber = '9012638716'
pickup_service.OriginDetail.PickupLocation.Address.StateOrProvinceCode = 'SC'
pickup_service.OriginDetail.PickupLocation.Address.PostalCode = '29631'
pickup_service.OriginDetail.PickupLocation.Address.CountryCode = 'US'
pickup_service.OriginDetail.PickupLocation.Address.StreetLines = ['155 Old Greenville Hwy', 'Suite 103']
pickup_service.OriginDetail.PickupLocation.Address.City = 'Clemson'
# pickup_service.OriginDetail.PickupLocation.Address.UrbanizationCode = ''  # For Puerto Rico only
pickup_service.OriginDetail.PickupLocation.Address.Residential = False

# FRONT, NONE, REAR, SIDE
# pickup_service.OriginDetail.PackageLocation = 'NONE'

# APARTMENT, BUILDING, DEPARTMENT, FLOOR, ROOM, SUITE
# pickup_service.OriginDetail.BuildingPart = 'SUITE'

# Identifies the date and time the package will be ready for pickup by FedEx.
pickup_service.OriginDetail.ReadyTimestamp = datetime.datetime.now().replace(microsecond=0).isoformat()

# Identifies the latest time at which the driver can gain access to pick up the package(s)
pickup_service.OriginDetail.CompanyCloseTime = '23:00:00'

pickup_service.CarrierCode = 'FDXE'

pickup_service.TotalWeight.Units = 'LB'
pickup_service.TotalWeight.Value = '1'
pickup_service.PackageCount = '1'
# pickup_service.OversizePackageCount = '1'

# pickup_service.CommodityDescription = ''

# DOMESTIC or INTERNATIONAL
# pickup_service.CountryRelationship = 'DOMESTIC'

# See PickupServiceCategoryType
# pickup_service.PickupServiceCategory = 'FEDEX_DISTANCE_DEFERRED'

pickup_service.send_request()

print pickup_service.response.HighestSeverity == 'SUCCESS'
print pickup_service.response.Notifications[0].Message
