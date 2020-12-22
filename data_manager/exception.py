from rest_framework.exceptions import APIException


class DuplicateNameException(APIException):
    status_code = 400

    def __init__(self, code_list=""):
        self.default_detail = "Duplicate name found found {user_code}".format(
            user_code=', '.join(code_list)
        )
        super().__init__()
