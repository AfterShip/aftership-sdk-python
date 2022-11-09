import requests

from urllib.parse import urljoin
from urllib.parse import urlparse
from aftership.hmac.hmac import Hmac

from aftership.signstring.signstring import SignString

from .const import AFTERSHIP_API_KEY, API_ENDPOINT, API_VERSION, AS_SIGNATURE_HMAC_SHA256, AS_API_KEY, CONTENT_TYPE, SIGNATURE_AES_HMAC_SHA256 
from .util import get_api_key, get_api_secret


def build_request_url(path):
    return urljoin(API_ENDPOINT, path)


def make_request(method, path, **kwargs):
    url = build_request_url(path)
    res = urlparse(url)
    params = kwargs.get('params', None)
    path = res.path

    params_str = ""
    if params:
       params_str = '&'.join([ str(key)+'='+str(value) for key,value in params.items()])

    if not path.startswith("/"):
        path = '/' + path

    if len(params_str)>0:
        path = '{}?{}'.format(path, params_str)

    signature_type = kwargs.pop('signature_type', None)
    if signature_type is None:
        return request_with_token(method, url, **kwargs)

    body = kwargs.get('json', None)
    content_type = None
    if (method == "POST" or method == "PUT" or method == "PATCH") and body is not None:
        content_type = CONTENT_TYPE
    
    # if using SignString, you must use AS_API_KEY header
    if signature_type == SIGNATURE_AES_HMAC_SHA256:
        return request_with_aes_hmac256_signature(method, url, path, content_type, **kwargs)
    
    return None


def request_with_token(method, url, **kwargs):
    headers = kwargs.pop('headers', dict())
    if headers.get(AFTERSHIP_API_KEY) is None and headers.get(AS_API_KEY) is None:
        headers[AFTERSHIP_API_KEY] = get_api_key()
    
    kwargs['headers'] = headers
    return requests.request(method, url, **kwargs)

def request_with_aes_hmac256_signature(method, url, path, content_type, **kwargs):
    headers = kwargs.pop('headers', dict())
    if headers.get(AS_API_KEY, None) is None:
        headers[AS_API_KEY] = get_api_key()

    body = kwargs.get('json', None)
    date, sign_string = gen_sign_string(method, path, body, headers, content_type)

    hmac = Hmac(get_api_secret())
    hmac_signature = hmac.hmac_signature(sign_string)
    headers[AS_SIGNATURE_HMAC_SHA256] = hmac_signature
    headers['Date'] = date

    if content_type is not None:
        headers["Content-Type"] = content_type

    kwargs['headers'] = headers
    return requests.request(method, url, **kwargs)

def gen_sign_string(method, path, body, headers, content_type):
    s = SignString(headers[AS_API_KEY])
    return s.gen_sign_string(method, path, body, headers, content_type)
