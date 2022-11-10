from unittest import TestCase

import aftership
import pytest

from aftership.util import get_aftership_api_key, get_as_api_secret


class UtilsTestCase(TestCase):
    @pytest.mark.vcr()
    def test_get_key(self):
        api_key = '12345678'
        aftership.api_key = api_key
        self.assertEqual(aftership.api_key, api_key)
        self.assertEqual(aftership.api_key, get_aftership_api_key())

    @pytest.mark.vcr()
    def test_get_secret(self):
        api_secret = '12345678'
        aftership.api_secret = api_secret
        self.assertEqual(aftership.api_secret, api_secret)
        self.assertEqual(aftership.api_secret, get_as_api_secret())
