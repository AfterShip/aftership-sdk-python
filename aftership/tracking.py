from .request import make_request
from .response import process_response
from .util import _build_tracking_url


def create_tracking(tracking, **kwargs):
    """Create a tracking.
    """
    response = make_request('POST', 'trackings', json=dict(tracking=tracking), **kwargs)
    return process_response(response)


def get_tracking(*, tracking_id=None, slug=None, tracking_number=None,
                 **kwargs):
    """Create a tracking.
    """
    optional_keys = ('tracking_postal_code', 'tracking_ship_date', 'tracking_account_number', 'tracking_key',
                     'tracking_origin_country', 'tracking_destination_country', 'tracking_state',
                     'fields', 'lang')
    params = {key: kwargs.pop(key) for key in optional_keys if key in kwargs}
    url = 'trackings/{}'.format(_build_tracking_url(tracking_id, slug, tracking_number))
    response = make_request('GET', url, params=params, **kwargs)
    return process_response(response)


def update_tracking(*, tracking, tracking_id=None, slug=None, tracking_number=None, **kwargs):
    """Update a tracking.
    """
    url = 'trackings/{}'.format(_build_tracking_url(tracking_id, slug, tracking_number))
    response = make_request('PUT', url, json=dict(tracking=tracking), **kwargs)
    return process_response(response)


def retrack(*, tracking_id=None, slug=None, tracking_number=None, **kwargs):
    """Retrack an expired tracking. Max 3 times per tracking.
    """
    url = 'trackings/{}/retrack'.format(_build_tracking_url(tracking_id, slug, tracking_number))
    response = make_request('POST', url, **kwargs)
    return process_response(response)


def get_last_checkpoint(*, tracking_id=None, slug=None, tracking_number=None, **kwargs):
    """Return the tracking information of the last checkpoint of a single tracking.
    """
    url = 'last_checkpoint/{}'.format(_build_tracking_url(tracking_id, slug, tracking_number))
    response = make_request('GET', url, **kwargs)
    return process_response(response)


def delete_tracking(*, tracking_id=None, slug=None, tracking_number=None, **kwargs):
    """Delete a tracking.
    """
    url = 'trackings/{}'.format(_build_tracking_url(tracking_id, slug, tracking_number))
    response = make_request('DELETE', url, **kwargs)
    return process_response(response)


def list_trackings(**kwargs):
    """Get tracking results of multiple trackings.
    """
    optional_keys = ('page', 'limit', 'keyword', 'slug', 'delivery_time', 'origin',
                     'destination', 'tag', 'created_at_min', 'created_at_max',
                     'fields', 'lang')

    params = {key: kwargs.pop(key) for key in optional_keys if key in kwargs}

    response = make_request('GET', 'trackings', params=params, **kwargs)
    return process_response(response)
