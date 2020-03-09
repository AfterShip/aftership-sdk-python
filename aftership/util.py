import logging
import os

import aftership

logger = logging.getLogger("aftership")


def _build_tracking_url(tracking_id, slug, tracking_number):
    if tracking_id and (slug or tracking_number):
        raise ValueError('Cannot specify tracking number and tracking id at the same time')
    elif tracking_id:
        url = '{}'.format(tracking_id)
    elif slug and tracking_number:
        url = '{}/{}'.format(slug, tracking_number)
    else:
        raise ValueError('You must specify the tracking number of tracking id')
    return url


def get_api_key():
    """Get AfterShip API key"""
    if aftership.api_key is not None:
        return aftership.api_key
    return os.getenv('AFTERSHIP_API_KEY')
