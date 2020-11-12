import re
import json
from io import BytesIO

from rest_framework import serializers
from rest_framework.fields import (
    get_attribute, is_simple_callable
)
import pytz
from PIL import Image

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from userapp.models import User


class CompressionImageField(serializers.ImageField):
    portrait_size = 1280, 720
    landscape_size = 720, 1280

    def _get_new_size(self, value):
        h, w = value.image.size
        if h > w:
            # if height is higher than it is a portrait
            return self.portrait_size
        else:
            return self.landscape_size

    def _needs_resize(self, value, size):
        h, w = value.image.size
        needs_scale = h > size[0] or w > size[1]

        one_mb = 1024 * 1024
        needs_resize = value.size > one_mb
        return needs_scale or needs_resize

    def to_internal_value(self, value):
        value = super().to_internal_value(value)
        h, w = value.image.size

        new_size = self._get_new_size(value)

        if self._needs_resize(value, new_size):
            output = BytesIO()

            image = Image.open(BytesIO(value.read()))
            image.thumbnail(new_size)
            image.save(output, format=image.format)

            value.file = output

        return value


class TzDateTimeField(serializers.DateTimeField):
    """
    Timezone aware DateTimeField for DRF.
    """

    def to_representation(self, obj):
        default_timezone = pytz.timezone(settings.TIME_ZONE)
        obj = obj.astimezone(default_timezone)
        date = super(TzDateTimeField, self).to_representation(obj)
        # format date here or just by pass above super call
        return date


def validate_name_length(value):
    if len(value) > 50:
        raise serializers.ValidationError("Name should not exceed 50 characters in length.")


def validate_delimiter(value, delimiter):
    """
    Ensure that delimiters such as hyphen, slash, comma don't
    fall at the start or end of the input value
    """
    message = "Separator ({}) must not be at the {} of the value."
    if value.startswith(delimiter):
        raise serializers.ValidationError(message.format(delimiter, "start"))

    if value.endswith(delimiter):
        raise serializers.ValidationError(message.format(delimiter, "end"))


def validate_yyyy_mm_dd(value):
    match = re.match('^(?P<year>\d{4})\-(?P<month>\d{1,2})\-(?P<day>\d{1,2})$', value)
    if match:
        d = match.groupdict()
        if int(d['month']) not in range(1, 13):
            raise serializers.ValidationError("Please enter a valid month.")

        if int(d['day']) not in range(1, 33):
            raise serializers.ValidationError("Please enter a valid day.")

        if int(d['year'][:2]) not in [19, 20]:
            raise serializers.ValidationError("Please enter a valid year.")
    else:
        raise serializers.ValidationError("Please enter a valid date in YYYY-MM-DD format.")
    return value


class DateCharField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs['min_length'] = 8
        kwargs['max_length'] = 10
        super().__init__(**kwargs)

    def to_internal_value(self, value):
        value = str(value).strip()
        validate_yyyy_mm_dd(value)
        return value


class HyphenAlphaNumericCharField(serializers.CharField):
    """
    This field only allows alphanumeric characters, hyphens and spaces.
    """

    def to_internal_value(self, value):
        value = str(value).strip()
        validate_delimiter(value, "-")

        if not value.replace(' ', '').replace('-', '').isalnum():
            raise serializers.ValidationError(
                "This field should contain alphabets, numbers, hyphen and space only."
            )
        return value


class NameField(serializers.CharField):
    def to_internal_value(self, name):
        name = name.strip()
        name = " ".join(map(lambda x: x.capitalize(), name.split()))
        validate_name_length(name)

        if not name.replace(' ', '').isalpha():
            raise serializers.ValidationError(
                "Name should contain alphabets and space only."
            )

        if not re.match("[a-zA-Z]{2,}(\s[a-zA-Z]{2,})+", name):
            raise serializers.ValidationError("Please pass full name.")

        return name


class CompanyNameField(HyphenAlphaNumericCharField):
    def to_internal_value(self, value):
        validate_name_length(value)
        return super().to_internal_value(value)


class RegNumberField(serializers.CharField):
    """
    Some numbers might contain hyphens and slashes such as
    citizenship number, company registration number etc.
    """

    def to_internal_value(self, value):
        value = str(value)
        if not value.replace(' ', '').replace('-', '').replace('/', '').isalnum():
            raise serializers.ValidationError(
                "This field can contain alphabets, numbers, hyphen and slash only."
            )

        if '-' in value and '/' in value:
            raise serializers.ValidationError("Please use either slash or hyphen and not both.")

        validate_delimiter(value, "-")
        validate_delimiter(value, "/")
        return value


class NumericCharField(serializers.CharField):
    """
    Fields such as PAN number
    """

    def to_internal_value(self, value):
        if not value.isnumeric():
            raise serializers.ValidationError(
                "This field can contain numeric characters only."
            )
        return value


class MobileField(serializers.CharField):
    def to_internal_value(self, mobile):
        if not len(str(mobile)) == 10:
            raise serializers.ValidationError("A mobile number should be 10 digit long.")

        if not re.match("9[678][0124568]\d{7}", str(mobile)):
            raise serializers.ValidationError("Invalid mobile number.")

        return mobile


class VirtualMobileField(serializers.CharField):
    def to_internal_value(self, mobile):
        if not len(str(mobile)) == 10:
            raise serializers.ValidationError(
                "Virtual mobile number must be 10 digits long."
            )

        if not settings.VIRTUAL_MOBILE_REGEX.match(str(mobile)):
            raise serializers.ValidationError(
                "Mobile number must have a 100 prefix."
            )
        return mobile


class PasswordField(serializers.CharField):
    def to_internal_value(self, password):
        if len(password) < 6:
            raise serializers.ValidationError("The password should at least be 6 characters long.")
        if len(password) > 20:
            raise serializers.ValidationError("The password should be shorter than 20 characters.")

        return password


class DetailRelatedField(serializers.RelatedField):
    """
    Read/write serializer field for relational field.
    Syntax:
        DetailRelatedField(Model, [lookup], representation)

        Model: model to which the serializer field is related to
        lookup: field for getting a model instance, if not supplied it defaults to idx
        representation: a model instance method name for getting serialized data
    """

    def __init__(self, model, **kwargs):
        if not kwargs.get("read_only"):
            kwargs["queryset"] = model.objects.all()

        self.lookup = kwargs.pop("lookup", None) or "idx"
        self.specify_object = kwargs.pop("specify_object", False)
        self.is_obsolete = kwargs.pop("is_obsolete", None)
        try:
            self.representation = kwargs.pop("representation")
        except KeyError:
            raise Exception("Please supply representation.")

        super(DetailRelatedField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            if isinstance(type(data), self._kwargs.get('model')):
                return data
            return self.queryset.get(**{self.lookup: data})
        except ObjectDoesNotExist:
            _error_msg = "Object does not exist."
            if self.specify_object:
                _error_msg = "Object \"{}\" does not exist.".format(data)
            raise serializers.ValidationError(_error_msg)

    def to_representation(self, obj):
        if self.representation == 'object':
            return obj
        request = None
        if self.context:
            request = self.context.get('request', None)
            if request:
                return getattr(obj, self.representation)(request)
        return getattr(obj, self.representation)()


class SpecificFieldsMixin(object):
    """
    Returns fields specified in query params 'fields'.
    """

    def __init__(self, *args, **kwargs):
        super(SpecificFieldsMixin, self).__init__(*args, **kwargs)

        if not self.context or not self.context.get("request"):
            return

        if self.context.get("request").method != "get":
            return

        fields = self.context["request"].query_params.get("fields")
        if fields:
            fields = fields.split(",")
            requested_fields = set(fields)
            available_fields = set(self.fields.keys())
            for field_name in available_fields - requested_fields:
                self.fields.pop(field_name)


class IDXOnlyObject:
    def __init__(self, idx):
        self.idx = idx

    def __str__(self):
        return "%s" % self.idx


class FRelatedField(serializers.PrimaryKeyRelatedField):
    default_error_messages = {
        'required': _('This field is required.'),
        'does_not_exist': _('Invalid idx "{pk_value}" - object does not exist.'),
        'incorrect_type': _('Incorrect type. Expected idx value, received {data_type}.'),
    }

    def get_attribute(self, instance):
        if self.use_pk_only_optimization() and self.source_attrs:
            # Optimized case, return a mock object only containing the pk attribute.
            try:
                instance = get_attribute(instance, self.source_attrs[:-1])
                value = instance.serializable_value(self.source_attrs[-1])
                if is_simple_callable(value):
                    # Handle edge case where the relationship `source` argument
                    # points to a `get_relationship()` method on the model
                    value = value().idx
                else:
                    value = getattr(instance, self.source_attrs[-1]).idx
                return IDXOnlyObject(idx=value)
            except AttributeError:
                pass

    def to_representation(self, obj):
        return obj.idx

    def to_internal_value(self, data):
        try:
            return self.queryset.get(idx=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)


class I18NField(serializers.CharField):
    """
    Converts i18n key-string to user selected language.
    """

    def to_representation(self, key_string):
        return __(key_string)


class JSONField(serializers.CharField):
    def to_representation(self, data):
        return json.loads(data)


class UsernameField(serializers.CharField):

    def to_internal_value(self, username):

        if len(username) < 6:
            raise serializers.ValidationError("The username should at least be 6 characters long.")
        if len(username) > 50:
            raise serializers.ValidationError("The username should be shorter than 50 characters.")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("The username already exists")

        return username


class EmailField(serializers.EmailField):

    def to_internal_value(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("The email already exists")

        return email


# class LowestLevelField(serializers.RelatedField):
#
#     def to_internal_value(self, id):
#         try:
#             return Level3.objects.get(id=id)
#         except Level3.DoesNotExist:
#             raise serializers.ValidationError("Doesn't exists")
#
#     def to_representation(self, value):
#         return {
#                 'id': value.id,
#                 'name': value.name,
#                 'level2': {
#                     'id': value.level2.id,
#                     'name': value.level2.name,
#                     'level3': {
#                         'id': value.level1.id,
#                         'name': value.level1.name
#                     }
#                 }
#         }
def request_context(self):
    request = None
    try:
        request = self.context['request']
    except:
        raise serializers.ValidationError("There is no request context in serializer.")
    return request


def file_representation(self, value):
    from go_print.settings import PROXY_URL

    if not value:
        return None

    use_url = getattr(self, 'use_url', True)
    if use_url:
        try:
            url = value.url
        except AttributeError:
            return None
        build_url = PROXY_URL + url
        # request = self.context.get('request', None)
        # if request is not None:
        #     build_url = request.build_absolute_uri(url)
        #     build_url = build_url.replace('192.168.88.15', 'demo.rosebayconsult.com')
        #     build_url = build_url.replace('127.0.0.1', 'demo.rosebayconsult.com')
        #     build_url = build_url.replace('localhost', 'demo.rosebayconsult.com')
        #     return build_url
        return build_url

    return value.name

class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid, os
        from modana.settings import MEDIA_ROOT

        # Check if this is a base64 string
        # Try to decode the file. Return validation error if it fails.
        request = request_context(self)
        try:
            if isinstance(data, six.string_types) or isinstance(data, bytes):
                # Check if the base64 string is in the "data:" format
                if isinstance(data, six.string_types):
                    if 'data:' in data and ';base64,' in data:
                        # Break out the header from the base64 content
                        header, data = data.split(';base64,')
                decoded_file = base64.b64decode(data)
                # Generate file name:
                file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
                # Get the file name extension:
                file_extension = self.get_file_extension(file_name, decoded_file)

                complete_file_name = "%s.%s" % (file_name, file_extension, )

                data = ContentFile(decoded_file, name=complete_file_name)
        except Exception as e:
            from django.core.files import File
            # raise serializers.ValidationError({'detail': str(e)})
            file_path = str(data)

            file_path = file_path.replace(request.get_host(), '')
            file_path = file_path.replace('http://', '')
            file_path = file_path.replace('https://', '')
            file_path = file_path.replace('/media', '')
            complete_file_name = file_path.split('/')[-1]
            file_path = MEDIA_ROOT + file_path
            data = None
            if os.path.exists(file_path):
                data = open(file_path, 'rb')
                # encoded_string = base64.b64encode(data.read())
                # decoded_file = base64.b64decode(encoded_string)
                os.remove(file_path)
                data = File(data, name=complete_file_name)
                # data = ContentFile(decoded_file, name=complete_file_name)
            return data
        else:
            return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

    def to_representation(self, value):
        value = file_representation(self, value)
        return value


class ImageFieldWithURL(serializers.ImageField):

    def to_internal_value(self, data):
        import os
        from go_print.settings import MEDIA_ROOT

        request = request_context(self)
        if isinstance(data, str):
            return data
        return super(ImageFieldWithURL, self).to_internal_value(data)

    def to_representation(self, value):
        value = file_representation(self, value)
        return value


class FileFieldWithURL(serializers.FileField):

    def to_internal_value(self, data):
        import os
        from go_print.settings import MEDIA_ROOT

        request = request_context(self)
        if isinstance(data, str):
            return data
        return super(FileFieldWithURL, self).to_internal_value(data)

    def to_representation(self, value):
        value = file_representation(self, value)
        return value


class RoundUpInteger(serializers.IntegerField):

    def to_representation(self, value):
        value = round(value, 2)
        return value


class RoundUpFloat(serializers.FloatField):

    def to_representation(self, value):
        value = round(value, 2)
        return value
