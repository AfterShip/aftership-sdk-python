from urllib.parse import urljoin

import requests

from .const import API_KEY_FILED_NAME, API_ENDPOINT
from .util import get_api_key


def build_request_url(path):
    return urljoin(API_ENDPOINT, path)


def make_request(method, path, **kwargs):
    url = build_request_url(path)

    headers = kwargs.pop('headers', dict())
    if headers.get(API_KEY_FILED_NAME) is None:
        headers[API_KEY_FILED_NAME] = get_api_key()
    kwargs['headers'] = headers
    return requests.request(method, url, **kwargs)
