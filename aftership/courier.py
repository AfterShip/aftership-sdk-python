from .request import make_request
from .response import process_response

__all__ = ['list_couriers', 'list_all_couriers', 'detect_courier']


def list_couriers(**kwargs):
    """Return a list of couriers activated at your AfterShip account.
    """
    response = make_request('GET', 'couriers', **kwargs)
    return process_response(response)


def list_all_couriers(**kwargs):
    """Return a list of all couriers.
    """
    response = make_request('GET', 'couriers/all', **kwargs)
    return process_response(response)


def detect_courier(tracking, **kwargs):
    """Return a list of matched couriers based on tracking number format and
    selected couriers or a list of couriers.
    """
    response = make_request('POST', 'couriers/detect', json=dict(tracking=tracking), **kwargs)
    return process_response(response)
