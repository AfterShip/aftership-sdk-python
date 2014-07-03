import json
import time
import threading
import datetime
import requests
import dateutil.parser


__author__ = 'Fedor Korshunov <mail@fedor.cc>'


# Values for test described in APIv3 class definition below.
# To run test cases go to the directory with current file and run:
# $ python __init__.py
TEST_SLUG = 'dpd-uk'
TEST_TRACKING_NUMBER = '15502370264989N'
TEST_API_KEY = 'YOUR_API_KEY'


class APIRequestException(Exception):
    def __getitem__(self, attribute):
        return self.args[0][attribute]


class APIv3RequestException(APIRequestException):
    def code(self):
        return self['meta']['code']

    def type(self):
        return self['meta']['error_type']

    def message(self):
        return self['meta']['error_message']

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
    def __init__(self, key=None,
                 max_calls_per_sec=10,
                 base_url='https://api.aftership.com',
                 ver='v3', headers={}):
        self._last_call = None
        self._rate_limit = 1.0 / float(max_calls_per_sec)

        self._headers = headers
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

        with threading.Lock():
            if self._last_call:
                delta = self._rate_limit - (time.clock() - self._last_call)
                if delta > 0:
                    time.sleep(delta)
            self._last_call = time.clock()

        response = requests.request(method, url, headers=headers,
                                    params=params, data=body)
        ret = json.loads(response.text)

        if not response.ok:
            raise APIRequestException(ret)

        return ret


class APIv3(API):
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
    u'dpd-uk'
    """
    def __init__(self, key, max_calls_per_sec=10, datetime_convert=True):
        self._datetime_fields = ['created_at',
                                 'created_at_min',
                                 'created_at_max',
                                 'updated_at',
                                 'expected_delivery',
                                 'checkpoint_time']
        self._datetime_convert = datetime_convert
        API.__init__(self, key, max_calls_per_sec=max_calls_per_sec,
                     base_url='https://api.aftership.com',
                     ver='v3', headers={})

    def _is_datetime(self, key, value):
        if type(value) is unicode and key in self._datetime_fields:
            return True
        return False

    def _convert_datetime_dict(self, dct):
        for key, value in dct.iteritems():

            # Convert ISO 8601 strings to datetime
            if self._is_datetime(key, value):
                dct[key] = dateutil.parser.parse(value)

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
            for key, value in body.iteritems():
                # Convert datetime to ISO 8601 string
                if type(value) is datetime.datetime:
                    value = value.replace(microsecond=0)
                    body[key] = value.isoformat()

                # Convert array of values to comma-separated string
                elif type(value) is list:
                    body[key] = u','.join(value)

            response = API.call(self, *args, **body)['data']

            # Convert ISO 8601 strings to datetime
            if self._datetime_convert:
                self._convert_datetime_dict(response)

            return response
        except APIRequestException as error:
            raise APIv3RequestException(*error.args)


if __name__ == "__main__":
    import doctest
    print 'Running tests...'
    doctest.testmod(extraglobs={'api': APIv3(TEST_API_KEY),
                                'slug': TEST_SLUG,
                                'number': TEST_TRACKING_NUMBER})
    print '\tdone!'