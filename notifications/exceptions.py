from rest_framework.exceptions import APIException


class DeviceException(APIException):
    status_code = 400
    default_detail = 'Device id not found'
