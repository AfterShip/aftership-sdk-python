from unittest import TestCase

import pytest

import aftership


class TrackingTestCase(TestCase):
    def setUp(self):
        self.slug = '4px'
        self.tracking_number = 'HH19260817'
        self.tracking_id = 'k5lh7dy7vvqeck71p5loe011'

    @pytest.mark.vcr()
    def test_create_tracking(self):
        response = aftership.tracking.create_tracking(tracking={'slug': self.slug,
                                                                'tracking_number': self.tracking_number})

    @pytest.mark.vcr()
    def test_get_tracking(self):
        response = aftership.tracking.get_tracking(slug=self.slug,
                                                   tracking_number=self.tracking_number)

    # @pytest.mark.vcr()
    # def test_delete_tracking(self):
    #     response = aftership.tracking.delete_tracking(slug='china-ems',tracking_number='1234567890')

    @pytest.mark.vcr()
    def test_list_trackings(self):
        response = aftership.tracking.list_trackings(slug=self.slug, limit=1)

    @pytest.mark.vcr()
    def test_update_tracking(self):
        response = aftership.tracking.update_tracking(tracking_id=self.tracking_id,
                                                      tracking={'title': 'new title'})

    @pytest.mark.vcr()
    def test_retrack(self):
        response = aftership.tracking.retrack(tracking_id=self.tracking_id)

    @pytest.mark.vcr()
    def test_get_last_checkpoint(self):
        response = aftership.tracking.get_last_checkpoint(tracking_id=self.tracking_id)
