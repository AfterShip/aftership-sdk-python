from urllib.parse import urljoin
import hashlib
from email.utils import formatdate
import hmac
import base64

import requests

from .const import API_KEY_FILED_NAME, API_ENDPOINT, API_VERSION
from .util import get_api_key, get_api_secret_key


def build_request_url(path):
    return urljoin(API_ENDPOINT, path)


def generate_date_rfc1123():
    return formatdate(timeval=None, localtime=False, usegmt=True)


def sign_request(method, path, headers, content):
    sign_string = generate_sign_string(method, path, headers, content)
    signature = hmac.new(get_api_secret_key().encode(), msg=sign_string.encode(), digestmod=hashlib.sha256)
    b64_signature = base64.b64encode(signature.digest()).decode()

    headers['as-signature-hmac-sha256'] = b64_signature


def generate_sign_string(method, path, headers, content):
    content_md5 = hashlib.md5(content).upper() if content else ''
    content_type = 'application/json' if content else ''
    date = generate_date_rfc1123()
    as_headers = {
        k.lower().strip(): v.strip()
        for k, v in sorted(headers.items())
        if k.lower().startswith('as-')
    }
    canonicalized_headers = ''
    if as_headers:
        canonicalized_headers = ''.join([f'{k}:{v}' for k, v in as_headers.items()])
    canonicalized_resource = f'/{API_VERSION}/{path}'

    headers['date'] = date
    headers['content-type'] = content_type

    return '\n'.join((method, content_md5, content_type, date,
                      canonicalized_headers, canonicalized_resource))


def make_request(method, path, **kwargs):
    url = build_request_url(path)

    headers = kwargs.pop('headers', dict())
    if headers.get(API_KEY_FILED_NAME) is None:
        headers[API_KEY_FILED_NAME] = get_api_key()

    if get_api_secret_key():
        sign_request(method, path, headers, kwargs.get('json'))

    kwargs['headers'] = headers
    return requests.request(method, url, **kwargs)
