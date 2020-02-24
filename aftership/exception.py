class AfterShipError(Exception):
    def __init__(self, message=None, code=None,
                 http_status=None, response=None,
                 ):
        super(AfterShipError, self).__init__()
        self.message = message
        self.code = code
        self.http_status = http_status
        self.response = response

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self.message)


class BadRequest(AfterShipError):
    pass


class Unauthorized(AfterShipError):
    pass


class Forbidden(AfterShipError):
    pass


class NotFound(AfterShipError):
    pass


class TooManyRequests(AfterShipError):
    pass


class InternalError(AfterShipError):
    pass


class UnexpectedError(AfterShipError):
    pass
