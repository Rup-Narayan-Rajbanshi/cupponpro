from rest_framework.exceptions import ValidationError


class UniqueTogetherValidatorMixin(object):
    """

        The class checks unique together validation for is_obsolete false cases.

        -> unique_together_fields is iterable of iterable i.e list of list or list of tuple or tuple of tuple ....

        -> from_request_fields are the fields that are get through request variable rather than attrs like user instance
            .......

        If you want any attribute from self.context['request'] just send it in dictionary format {
            'value_from_context_request': 'field_name'
        } eg. {'user': 'user'} or {'user.owner': 'company'}


    """

    unique_together_fields = None
    from_request_fields = None

    def validate(self, attrs):
        allowed_from_request_fields = ['user', 'user.owner']

        assert self.unique_together_fields is not None, "Unique together with company requires other field"
        assert self.from_request_fields is None or len(
                set(self.from_request_fields.keys()) - set(allowed_from_request_fields)
        ) == 0, "Allowed fields from requests are {}".format(allowed_from_request_fields)

        for unique_together in self.unique_together_fields:

            lookup = {
                "is_obsolete": False,
            }

            if self.from_request_fields:
                request = self.context['request']

                for request_field in self.from_request_fields:
                    attr_value = request
                    for attr in request_field.split('.'):
                        attr_value = getattr(attr_value, attr)

                    lookup[self.from_request_fields[request_field]] = attr_value

            fields = []
            for lookup_expr in unique_together:
                field = lookup_expr.split("__")[0] if "__" in lookup_expr else lookup_expr
                fields.append(field)
                lookup[lookup_expr] = attrs[field]

            if self.instance is not None:
                if self.Meta.model.objects.filter(**lookup).exclude(id=self.instance.id).exists():
                    raise ValidationError({
                        "detail": "The given input for the fields {} already exists".format(
                                ', '.join(fields).title())
                        }
                    )
            else:
                if self.Meta.model.objects.filter(**lookup).exists():
                    raise ValidationError({
                        "detail": "The given input for the fields {} already exists".format(
                            ', '.join(fields).title())
                        }
                    )

        return super().validate(attrs)


class CustomValidationMessageForSerializerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].error_messages['required'] = "{} is required.".format(
                    field.replace('_', ' ').capitalize())
