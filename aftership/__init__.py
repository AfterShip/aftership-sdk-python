import requests
import json
import time
import threading

__author__ = 'Fedor Korshunov <mail@fedor.cc>'


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
                 max_calls_per_sec=10.0,
                 base_url='https://api.aftership.com',
                 ver='v3',
                 headers={}):

        self._last_call = None
        self._rate_limit = 1.0 / float(max_calls_per_sec)

        self._headers = headers
        if key:
            self._headers['aftership-api-key'] = key
        self._api_url = '%s/%s' % (base_url, ver)

        RequestPart.__init__(self, base=self)

    def call(self, method, path, *args, **body):
        args = ('/%s' % '/'.join(args)) if args else ''
        url = '%s%s%s' % (self._api_url, args, path)

        headers = self._headers
        if method != 'get':
            headers['Content-Type'] = 'application/json'
            params = {}
        elif body:
            params = body
            body = {}

        with threading.Lock():
            if self._last_call:
                delta = self._rate_limit - (time.clock() - self._last_call)
                if delta > 0:
                    time.sleep(delta)
            self._last_call = time.clock()

        response = requests.request(method, url,
                                    headers=headers,
                                    params=params,
                                    data=json.dumps(body))
        return json.loads(response.text)