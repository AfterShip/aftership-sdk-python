import requests
from urllib.parse import urljoin
from urllib.parse import urlparse
from aftership.hmac.hmac import Hmac
from aftership.rsa.rsa import Rsa

from aftership.signstring.signstring import SignString

from .const import API_KEY_FILED_NAME, API_ENDPOINT, AS_SIGNATURE_HMAC_SHA256, AS_SIGNATURE_RSA_SHA256, AS_API_KEY, CONTENT_TYPE, SIGNATURE_AES_HMAC_SHA256, SIGNATURE_RSA_HMAC_SHA256 
from .util import get_api_key, get_api_secret


def build_request_url(path):
    return urljoin(API_ENDPOINT, path)


def make_request(method, path, **kwargs):
    url = build_request_url(path)
    res = urlparse(url)
    path = res.path
    if  len(res.params)>0:
        path = '{}?{}'.format(res.path, res.params)

    signature_type = kwargs.pop('signature_type', None)
    if signature_type is None:
        return request_with_token(method, url, **kwargs)
    
    body = kwargs.get('json', None)
    content_type = None
    if (method == "POST" or method == "PUT") and body is not None:
        content_type = CONTENT_TYPE
    
    res = urlparse(url)
    path = res.path
    if  len(res.params)>0:
        path = '{}?{}'.format(res.path, res.params)

    # if using SignString, you must use AS_API_KEY header
    if signature_type == SIGNATURE_AES_HMAC_SHA256:
        return request_with_aes_hmac256_signature(method, url, path, content_type, **kwargs)
    
    if signature_type == SIGNATURE_RSA_HMAC_SHA256:
        return request_with_rsa_hmac256_signature(method, url, path, content_type, **kwargs)

    return None


def request_with_token(method, url, **kwargs):
    headers = kwargs.pop('headers', dict())
    if headers.get(API_KEY_FILED_NAME) is None:
        headers[API_KEY_FILED_NAME] = get_api_key()
    elif headers.get(AS_API_KEY) is None:
        headers[AS_API_KEY] = get_api_key()

    kwargs['headers'] = headers
    return requests.request(method, url, **kwargs)

def request_with_aes_hmac256_signature(method, url, path, content_type, **kwargs):
    headers = kwargs.pop('headers', dict())
    if headers.get(AS_API_KEY, None) is None:
        headers[AS_API_KEY] = get_api_key()

    headers['as-store-id'] = 'dyson-production-sandbox-store'
    
    body = kwargs.get('json', None)
    date, sign_string = gen_sign_string(method, path, body, headers, content_type)

    print("aes_private_key========", get_api_secret())
    print('sign_string=====', sign_string)

  
    hmac = Hmac(get_api_secret())
    hmac_signature = hmac.hmac_signature(sign_string)
    print('hmac_signature=====', hmac_signature)

    headers[AS_SIGNATURE_HMAC_SHA256] = hmac_signature
    headers['Date'] = date

    if content_type is not None:
        headers["Content-Type"] = content_type

    kwargs['headers'] = headers
    return requests.request(method, url, **kwargs)


def request_with_rsa_hmac256_signature(method, url, path, content_type, **kwargs):
    headers = kwargs.pop('headers', dict())
    if headers.get(AS_API_KEY, None) is None:
        headers[AS_API_KEY] = get_api_key()

    body = kwargs.get('json', None)
    rsa_private_key = kwargs.pop('rsa_private_key', None)
    if rsa_private_key is None:
        return None

    date, sign_string = gen_sign_string(method, path, body, headers, content_type)
    sign_string = 'abc'
    # sign_string = 'abc'
    print("rsa_private_key========", rsa_private_key)
    rsa = Rsa(rsa_private_key)
    rsa_signature = rsa.rsa_signature(sign_string)
    print('rsa_signature=====', rsa_signature)
    headers[AS_SIGNATURE_RSA_SHA256] = rsa_signature
    headers['Date'] = date
    kwargs['headers'] = headers
    if content_type is not None:
        headers["Content-Type"] = content_type
    rsa.verify(sign_string, rsa_signature)
    return requests.request(method, url, **kwargs)

def gen_sign_string(method, path, body, headers, content_type):
    s = SignString(headers[AS_API_KEY])
    return s.gen_sign_string(method, path, body, headers, content_type)
