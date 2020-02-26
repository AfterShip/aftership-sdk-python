from unittest import TestCase

import aftership
from aftership.util import get_api_key


class UtilsTestCase(TestCase):
    def test_get_key(self):
        api_key = '12345678'
        aftership.api_key = api_key
        self.assertEqual(aftership.api_key, api_key)
        self.assertEqual(aftership.api_key, get_api_key())
