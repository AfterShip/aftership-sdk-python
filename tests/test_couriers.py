from unittest import TestCase

import pytest

from aftership import courier


class CourierTestCase(TestCase):
    @pytest.mark.vcr()
    def test_get_couriers(self):
        resp = courier.list_couriers()
        self.assertIn('total', resp)
        self.assertIn('couriers', resp)

    @pytest.mark.vcr()
    def test_get_all_couriers(self):
        resp = courier.list_all_couriers()
        self.assertIn('total', resp)
        self.assertIn('couriers', resp)

    @pytest.mark.vcr()
    def test_detect_courier(self):
        resp = courier.detect_courier(tracking={'tracking_number': '1234567890'})
        self.assertIn('total', resp)
        self.assertIn('couriers', resp)
