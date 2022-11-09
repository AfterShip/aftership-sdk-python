# coding=utf-8

import os
import hashlib
import urllib
import time
import json
from urllib import parse
from typing import Union,Text,Dict

BODY = Union[Text,Dict]

class SignString():
    def __init__(self, api_secret:str):
        self.api_secret = api_secret
    
    def _gen_sign_string(self, method: str, body:BODY, content_type: str, date: str, canonicalized_as_headers: str,
                    canonicalized_resource: str) -> str:
        result = ''
        result += method + '\n'
        if body:
            if isinstance(body, dict):
                body = json.dumps(body)
            body = hashlib.md5(body.encode()).hexdigest().upper()
        else:
            body = ''
            content_type = ''

        result += body + '\n'
        result += content_type + '\n'
        result += date + '\n'
        result += canonicalized_as_headers + '\n'
        result += canonicalized_resource

        return result

    def _get_canonicalized_as_headers(self, headers: dict) -> str:
        new_header = {}
        for k, v in headers.items():
            new_key = k.lower()
            new_value = v.strip()
            new_header.update({new_key: new_value})

        new_header = dict(sorted(new_header.items()))

        result = '\n'.join([k + ':' + v for k, v in new_header.items()])
        return result
    
    def _get_canonicalized_resource(self, raw_url: str) -> str:
        url_parse_result = parse.urlsplit(raw_url)
        path = url_parse_result.path
        query = urllib.parse.urlencode(sorted(dict(parse.parse_qsl(url_parse_result.query)).items()))
        if query:
            path = path + '?' + query
        return path

    def gen_sign_string(self, method: str, uri: str, body: str, as_header: dict, content_type: str) -> tuple:
        if self.api_secret is None:
            self.api_secret = os.getenv('AFTERSHIP_API_SECRET')

        canonicalized_as_headers = self._get_canonicalized_as_headers(as_header)
        canonicalized_resource = self._get_canonicalized_resource(uri)

        date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
        sign_string = self._gen_sign_string(method=method, body=body, content_type=content_type, date=date,
                                    canonicalized_as_headers=canonicalized_as_headers,
                                    canonicalized_resource=canonicalized_resource)

        return date, sign_string