from rest_framework.exceptions import  APIException


class InvalidChangeStatusException(APIException):
    status_code = 400

    def __init__(self, object_name, frm, to):
        self.default_detail = 'Cannot change status from {} to {} for {}.'.format(
            frm, to, object_name
        )
        super().__init__()

class ServerTimeOutException(APIException):
    """
        For otp generation while checking if the generated is unique or not.
    """
    status_code = 504
    default_detail = 'Server time out for the requested operation. Please try again later.'


class InvalidRequestException(APIException):
    status_code = 400
    default_detail = 'Invalid request.'
