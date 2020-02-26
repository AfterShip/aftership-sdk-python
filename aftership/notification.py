from .request import make_request
from .response import process_response
from .util import _build_tracking_url


def list_notifications(*, tracking_id=None, slug=None, tracking_number=None, **kwargs):
    """ Get contact information for the users to notify when the tracking changes.
    Please note that only customer receivers will be returned. Any `email`, `sms`
    or `webhook` that belongs to the Store will not be returned.
    """
    url = 'notifications/{}'.format(_build_tracking_url(tracking_id, slug, tracking_number))
    response = make_request('GET', url, **kwargs)
    return process_response(response)


def add_notification(*, notification, tracking_id=None, slug=None, tracking_number=None, **kwargs):
    """Add notification receivers to a tracking number.
    """
    url = 'notifications/{}/add'.format(_build_tracking_url(tracking_id, slug, tracking_number))
    response = make_request('POST', url, json=dict(notification=notification), **kwargs)
    return process_response(response)


def remove_notification(*, notification, tracking_id=None, slug=None, tracking_number=None, **kwargs):
    """Remove notification receivers from a tracking number.
    """
    url = 'notifications/{}/remove'.format(_build_tracking_url(tracking_id, slug, tracking_number))
    response = make_request('POST', url, json=dict(notification=notification), **kwargs)
    return process_response(response)
