from rest_framework.exceptions import ValidationError
from helpers.exceptions import CustomAPIException
from rest_framework.exceptions import PermissionDenied
from autho.models import UserSetting


def localize_exception(func):
    def wrapper(request, *args, **kwargs):
        try:
            response = func(request, *args, **kwargs)
            return response
        except CustomAPIException as e:
            if request.user.is_anonymous:
                raise CustomAPIException(detail=e.default_detail_id, code=e.status_code)
            language = request.data.get('lang')
            if language == 'id':
                if e.default_detail_id:
                    raise CustomAPIException(detail=e.default_detail_id, code=e.status_code)
            else:
                raise e
        except ValidationError as e:
            raise e
    return wrapper
