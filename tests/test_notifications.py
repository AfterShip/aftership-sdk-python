from unittest import TestCase

import pytest

import aftership


class NotificationTestCase(TestCase):
    @pytest.mark.vcr()
    def test_list_notification(self):
        response = aftership.notification.list_notifications(tracking_id='k5lh7dy7vvqeck71p5loe011')

    @pytest.mark.vcr()
    def test_add_notification(self):
        response = aftership.notification.add_notification(tracking_id='k5lh7dy7vvqeck71p5loe011',
                                                           notification={'emails': ['jk.zhang@aftership.com']})

    @pytest.mark.vcr()
    def test_remove_notification(self):
        response = aftership.notification.remove_notification(tracking_id='k5lh7dy7vvqeck71p5loe011',
                                                              notification={'emails': ['support@aftership.com']})
