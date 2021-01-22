from rest_framework.exceptions import APIException


class DuplicateNameException(APIException):
    status_code = 400

    def __init__(self, name_list=""):
        self.default_detail = "Duplicate name found found {name}".format(
            name=', '.join(name_list)
        )
        super().__init__()


class ProductCategoryNotExistException(APIException):
    status_code = 400

    def __init__(self, category_list=""):
        self.default_detail = "ProductCategory does not exists {category}".format(
            category=', '.join(category_list)
        )
        super().__init__()


class ProductCategoryAlreadyExistException(APIException):
    status_code = 400

    def __init__(self, category_list=""):
        self.default_detail = "ProductCategory already exists {category}".format(
            category=', '.join(category_list)
        )
        super().__init__()


class ProductCodeAlreadyExistException(APIException):
    status_code = 400

    def __init__(self, category_list=""):
        self.default_detail = "Product Code already exists {category}".format(
            category=', '.join(category_list)
        )
        super().__init__()
