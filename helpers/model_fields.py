import re
from django.core.exceptions import ValidationError
from django.db.models import CharField, URLField


class URLValidator:

    def __call__(self, value):
        domain_name = '[A-Za-z0-9]+(\-[A-Za-z0-9]+)*'
        domain_ext = '(\.[A-Za-z]{2,8}(/)?){1,2}'
        full_domain = domain_name + domain_ext + '$'
        url_regex = r'((http|https)://' + full_domain + ')|(www\.' + full_domain + ')'
        if not re.match(url_regex, value):
            raise ValidationError("Enter a valid URL.", code=400)


class CustomURLField(CharField):
    default_validators = [URLValidator()]
