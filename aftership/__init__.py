from collections import defaultdict
import json
import time
import threading
import datetime
import requests
import dateutil.parser
import sys
import logging
from requests.exceptions import HTTPError


__author__ = 'AfterShip <support@aftership.com>'
__version__ = '0.1'


logger = logging.getLogger(__name__)


# Values for test described in APIv3 class definition below.
# To run test cases go to the directory with current file and run:
# $ python __init__.py
TEST_SLUG = 'russian-post'
TEST_TRACKING_NUMBER = '65600077151512'
TEST_API_KEY = 'YOUR_API_KEY'


py_ver = sys.version_info[0]

if py_ver == 3:
    unicode_type = str
else:
    unicode_type = unicode


class APIRequestException(Exception):
    def __init__(self, *args, **kwargs):
        super(APIRequestException, self).__init__(*args, **kwargs)
        if isinstance(self.args[0], dict):
            self._data = self.args[0]
        else:
            self._message = self.args[0]
            self._data = defaultdict(lambda : defaultdict(unicode_type))
            self._data['data'] = ''

    def __getitem__(self, attribute):
        return self._data[attribute]


class APIv3RequestException(APIRequestException):
    def code(self):
        return self['meta']['code']

    def type(self):
        return self['meta']['error_type']

    def message(self):
        return self['meta']['error_message'] or self._message

    def data(self):
        return self['data']


class APIv4RequestException(APIRequestException):
    def code(self):
        return self['meta']['code']

    def type(self):
        return self['meta']['type']

    def message(self):
        return self['meta']['message'] or self._message

    def data(self):
        return self['data']


class RequestPart(object):
    def __init__(self, path='', base=None):
        self._path = path
        self._base = base

    def __getitem__(self, attribute):
        return self.__getattr__(attribute)

    def __getattr__(self, chunk):
        return RequestPart('%s/%s' % (self._path, chunk), self._base)

    def request(self, method, *args, **body):
        return self._base.call(method, self._path, *args, **body)

    def get(self, *args, **body):
        return self.request('get', *args, **body)

    def post(self, *args, **body):
        return self.request('post', *args, **body)

    def put(self, *args, **body):
        return self.request('put', *args, **body)

    def delete(self, *args, **body):
        return self.request('delete', *args, **body)


class API(RequestPart):
    DEFAULT_HEADERS = {
        'User-Agent': 'aftership-python/{}'.format(__version__),
    }

    def __init__(self, key=None,
                 max_calls_per_sec=10,
                 base_url='https://api.aftership.com',
                 ver='v3', headers={}):
        self._last_call = None
        self._rate_limit = 1.0 / float(max_calls_per_sec)

        self._headers = self.DEFAULT_HEADERS
        self._headers.update(headers)
        if key:
            self._headers['aftership-api-key'] = key
        self._api_url = '%s/%s' % (base_url, ver)

        RequestPart.__init__(self, base=self)

    def call(self, method, path, *args, **body):
        args = ('/%s' % '/'.join(args)) if args else ''
        url = '%s%s%s' % (self._api_url, path, args)

        headers = self._headers
        params = None
        if method != 'get':
            headers['Content-Type'] = 'application/json'
            body = json.dumps(body)
        elif body:
            params = body
            body = None

        logger.debug('args: %s; url: %s; headers: %s', args, url, headers)

        with threading.Lock():
            if self._last_call:
                delta = self._rate_limit - (time.clock() - self._last_call)
                if delta > 0:
                    time.sleep(delta)
            self._last_call = time.clock()

        response = requests.request(method, url, headers=headers,
                                    params=params, data=body)
        try:
            response.raise_for_status()
            ret = response.json()
        except (HTTPError, ValueError) as error:
            logger.exception('Error in AfterShip response')
            raise APIRequestException(*error.args)

        return ret


class APIv3(API):
    def __init__(self, key, max_calls_per_sec=10, datetime_convert=True, _prefix='v3'):
        self._datetime_fields = ['created_at',
                                 'created_at_min',
                                 'created_at_max',
                                 'updated_at',
                                 'expected_delivery',
                                 'checkpoint_time',
                                 'tracking_ship_date',
                                 'expected_delivery']
        self._datetime_convert = datetime_convert
        API.__init__(self, key, max_calls_per_sec=max_calls_per_sec,
                     base_url='https://api.aftership.com',
                     ver=_prefix, headers={})

    def _is_datetime(self, key, value):
        if type(value) is unicode_type and key in self._datetime_fields and len(value) > 0:
            return True
        return False

    def _convert_datetime_dict(self, dct):
        if type(dct) is dict:
            # for key, value in dct.iteritems():
            for key in list(dct.keys()):
                value = dct[key]

                # Convert ISO 8601 strings to datetime
                if self._is_datetime(key, value):
                    try:
                        dct[key] = dateutil.parser.parse(value)
                    except:
                        dct[key] = value

                # Iterate thru dict
                elif type(value) is dict:
                    dct[key] = self._convert_datetime_dict(value)

                # Iterate thru list
                elif type(value) is list:
                    dct[key] = []
                    for item in value:
                        dct[key].append(self._convert_datetime_dict(item))

        return dct

    def call(self, *args, **body):
        try:
            # for key, value in body.iteritems():
            for key in list(body.keys()):
                value = body[key]

                # Convert datetime to ISO 8601 string
                if type(value) is datetime.datetime:
                    value = value.replace(microsecond=0)
                    body[key] = value.isoformat()

                # Convert array of values to comma-separated string
                elif type(value) is list:
                    body[key] = ','.join(value)

            response = API.call(self, *args, **body)['data']
            # pprint.pprint(response)

            # Convert ISO 8601 strings to datetime
            if self._datetime_convert:
                self._convert_datetime_dict(response)

            return response
        except APIRequestException as error:
            raise APIv3RequestException(*error.args)


class APIv4(APIv3):
    """
    Test code goes below.

    Test covers all accessing methods (POST, GET, PUT, DELETE).
    Test covers all variants of building specific API calls (endpoints paths + body):
    - dot.separated.constants.get()                : GET /dot/separated/constants
    - params['in']['brackets'].get()               : GET /params/in/brackets
    - path.get('arg1', 'arg2', arg_name='arg3')    : GET /path/arg1/arg2?arg_name=arg3
    Test checks conversion of input list type parameters to comma separated strings.
    Test checks conversion of input timestamp strings to datetime variables.
    Test checks conversion of output timestamp strings to datetime variables.


    >>> api.trackings.post(tracking=dict(slug=slug, tracking_number=number, title="Title"))['tracking']['title']
    u'Title'
    >>> api.trackings.get(slug, number, fields=['title', 'created_at'])['tracking']['title']
    u'Title'
    >>> type(api.trackings.put(slug, number, tracking=dict(title="Title (changed)"))['tracking']['updated_at'])
    <type 'datetime.datetime'>
    >>> api.trackings[slug][number].get()['tracking']['title']
    u'Title (changed)'
    >>> api.trackings.get(created_at_min=datetime.datetime(2014, 6, 1), fields=['title', 'order_id'])['fields']
    u'title,order_id'
    >>> api.trackings.delete(slug, number)['tracking']['slug']
    u'russian-post'
    """
    def __init__(self, key, max_calls_per_sec=10, datetime_convert=True, _prefix='v4'):
        APIv3.__init__(self, key,
                       max_calls_per_sec=max_calls_per_sec,
                       datetime_convert=datetime_convert,
                       _prefix=_prefix)

    def call(self, *args, **body):
        try:
            return APIv3.call(self, *args, **body)
        except APIv3RequestException as error:
            raise APIv4RequestException(*error.args)


if __name__ == "__main__":
    import doctest
    print("Running smoke tests")
    doctest.testmod(extraglobs={'slug': TEST_SLUG,
                                'number': TEST_TRACKING_NUMBER,
                                'api': APIv4(TEST_API_KEY)})
    print("done!")
