from unittest import TestCase

import aftership
from aftership.util import get_api_key, get_api_secret


class UtilsTestCase(TestCase):
    def test_get_key(self):
        api_key = '12345678'
        aftership.api_key = api_key
        self.assertEqual(aftership.api_key, api_key)
        self.assertEqual(aftership.api_key, get_api_key())

    def test_get_secret(self):
        api_secret = '12345678'
        aftership.api_secret = api_secret
        self.assertEqual(aftership.api_secret, api_secret)
        self.assertEqual(aftership.api_secret, get_api_secret())
