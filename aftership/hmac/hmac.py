# coding=utf-8

import os
import hashlib
import base64
import hmac

class Hmac():
    def __init__(self, api_secret):
        self.api_secret = api_secret
    
    def hmac_signature(self, sign_string: str) -> str:
        if self.api_secret is None:
            self.api_secret = os.getenv('AFTERSHIP_API_SECRET')
        signature_str = hmac.new(bytes(self.api_secret.encode()), msg=bytes(sign_string.encode()), digestmod=hashlib.sha256).digest()
        return base64.b64encode(signature_str).decode()