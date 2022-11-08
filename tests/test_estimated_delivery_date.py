from unittest import TestCase

import pytest

from aftership import estimated_delivery_date
from aftership import const



class EstimatedDeliveryDateTestCase(TestCase):
    @pytest.mark.vcr()
    def test_batch_predict_estimated_delivery_date(self):
        estimated_delivery_dates=[
                {
                    "slug": "fedex",
                    "service_type_name": "FEDEX HOME DELIVERY",
                    "origin_address": {
                        "country": "USA",
                        "state": "WA",
                        "postal_code": "98108",
                        "raw_location": "Seattle, Washington, 98108, USA, United States"
                    },
                    "destination_address": {
                        "country": "USA",
                        "state": "CA",
                        "postal_code": "92019",
                        "raw_location": "El Cajon, California, 92019, USA, United States"
                    },
                    "weight": {
                        "unit": "kg",
                        "value": 11
                    },
                    "package_count": 1,
                    "pickup_time": "2021-07-01 15:00:00",
                    "estimated_pickup": {
                        "order_processing_time": {},
                        "pickup_time": ""
                    }
                }
            ]
        resp = estimated_delivery_date.batch_predict_estimated_delivery_date(estimated_delivery_dates=estimated_delivery_dates)
        print(resp)
        resp = estimated_delivery_date.batch_predict_estimated_delivery_date(estimated_delivery_dates=estimated_delivery_dates, 
                                                                            signature_type=const.SIGNATURE_AES_HMAC_SHA256)
        print(resp)
        
