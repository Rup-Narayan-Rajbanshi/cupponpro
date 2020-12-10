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


class PhoneNumberNotFoundException(APIException):
    status_code = 400
    default_detail = "Phone number not found."


class OTPCoolDownException(APIException):
    status_code = 400
    default_detail = "You can only resend OTP once in 60 seconds."


class MaxResendOTPLimitReached(APIException):
    status_code = 400
    default_detail = "Maximum limit of resending OTP reached."


class InvalidOTPException(APIException):
    status_code = 400
    default_detail = "The otp entered is invalid."


class InvalidTokenException(APIException):
    status_code = 400
    default_detail = "The token given is invalid."


class PhoneNumberExistsException(APIException):
    status_code = 400
    default_detail = "Phone number exists already."


class OrderScanCooldownException(APIException):
    status_code = 400
    default_detail = "Please wait, someone is initializing the order."


class OrderSessionExpiredException(APIException):
    status_code = 408
    default_detail = "Session expired. Please scan again to order."
