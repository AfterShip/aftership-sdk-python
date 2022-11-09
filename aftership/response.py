import json

from .exception import BadRequest, Forbidden, NotFound, Unauthorized, TooManyRequests, InternalError, UnexpectedError

error_mapping = {
    'BadRequest': BadRequest,
    'Unauthorized': Unauthorized,
    'Forbidden': Forbidden,
    'NotFound': NotFound,
    'TooManyRequests': TooManyRequests,
    'InternalError': InternalError,
}


def process_response(response):
    try:
        json_content = response.json()
    except json.JSONDecodeError:
        raise InternalError

    if response.status_code // 100 == 2:
        return json_content['data']

    error_type = json_content['meta']['type']

    if error_type in error_mapping:
        error_cls = error_mapping[error_type]
    else:
        error_cls = UnexpectedError

    raise error_cls(message=json_content['meta']['message'],
                    code=json_content['meta']['code'],
                    http_status=response.status_code,
                    response=response,
                    )
