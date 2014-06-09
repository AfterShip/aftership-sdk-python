import requests
import json

__author__ = 'Fedor Korshunov <mail@fedor.cc>'


class RequestPart(object):
    def __init__(self, path, base=None):
        self._path = path
        self._base = base

    def __getitem__(self, attribute):
        return self.__getattr__(attribute)

    def __getattr__(self, chunk):
        return RequestPart('%s/%s' % (self._path if self._path else '', chunk),
                           self._base)

    def get(self, **body):
        return self._base.call('get', self._path, **body)

    def post(self, **body):
        return self._base.call('post', self._path, **body)

    def put(self, **body):
        return self._base.call('put', self._path, **body)

    def delete(self, **body):
        return self._base.call('delete', self._path, **body)


class API(RequestPart):
    def __init__(self, key, base_url='https://api.aftership.com', ver='v3'):
        self._headers = {'aftership-api-key': key}
        self._api_url = '%s/%s' % (base_url, ver)
        RequestPart.__init__(self, None, base=self)

    def call(self, method, path, **body):
        url = u'%s%s' % (self._api_url, path)
        headers = self._headers
        params = {}

        if method != 'get':
            headers['Content-Type'] = 'application/json'
        elif body:
            params = body
            body = {}

        response = requests.request(method, url, headers=headers,params=params, data=json.dumps(body))
        return json.loads(response.text)