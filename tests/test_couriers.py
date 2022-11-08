from unittest import TestCase

import pytest

from aftership import courier
from aftership import const

body='{"source_id":"1710452100BO","name":"1710452100BO","number":"1710452100BO","currency":"EUR","status":"closed","financial_status":"paid","fulfillment_status":"fulfilled","order_total":"399","shipping_total":"0","tax_total":"63.71","discount_total":"0","subtotal":"335.29","items":[{"source_id":"230278-01","sku":"230278-01","quantity":1,"unit_weight":{"unit":"kg","value":8.06},"unit_price":"399","discount":"0","tax":"63.71","return_quantity":1,"fulfillable_quantity":1,"source_product_id":"230278-01","source_variant_id":"230278-01","title":"Cinetic Big Ball Multi Floor 2","hs_code":null,"origin_country_region":"DEU","image_urls":["https://dyson-h.assetsadobe2.com/is/image/content/dam/dyson/images/products/primary/230278-01.png"]}],"source_created_at":"2022-08-08T09:34:03.000Z","source_updated_at":"2022-08-08T09:34:03.000Z","customer":{"source_id":"1710452100BO","first_name":"MICH DE EU RETURNS","last_name":"MICH DE EU RETURNS","emails":["boononn.tang@dyson.com"],"phones":["3745345234"]},"shipping_address":{"first_name":"Boon","address_line_1":"Albrechtstrasse","city":"Oberhausen","state":"Nordrhein-Westfalen","country_region":"DEU","postal_code":"46145","phone":"3745345234"}}'


class CourierTestCase(TestCase):
    @pytest.mark.vcr()
    def test_get_couriers(self):
        resp = courier.list_couriers()
        self.assertIn('total', resp)
        self.assertIn('couriers', resp)

    @pytest.mark.vcr()
    def test_aes_get_couriers(self):
        resp = courier.list_couriers(signature_type=const.SIGNATURE_AES_HMAC_SHA256)
        self.assertIn('total', resp)
        self.assertIn('couriers', resp)


    @pytest.mark.vcr()
    def test_get_all_couriers(self):
        resp = courier.list_all_couriers()
        self.assertIn('total', resp)
        self.assertIn('couriers', resp)

    @pytest.mark.vcr()
    def test_aes_get_all_couriers(self):
        resp = courier.list_all_couriers(signature_type=const.SIGNATURE_AES_HMAC_SHA256)
        self.assertIn('total', resp)
        self.assertIn('couriers', resp)

    @pytest.mark.vcr()
    def test_detect_courier(self):
        resp = courier.detect_courier(tracking={"tracking_number": "1234567890"})
        self.assertIn('total', resp)
        self.assertIn('couriers', resp)

    @pytest.mark.vcr()
    def test_aes_detect_courier(self):
        resp = courier.detect_courier(signature_type=const.SIGNATURE_AES_HMAC_SHA256,
                                        tracking={"tracking_number": "1234567890"})
        self.assertIn('total', resp)
        self.assertIn('couriers', resp)