from django.db import transaction
from rest_framework import serializers

from helpers.exceptions import InvalidRequestException
from helpers.serializer_fields import FRelatedField
from helpers.serializer_mixins import CustomValidationMessageForSerializerMixin


class CustomModelSerializer(CustomValidationMessageForSerializerMixin, serializers.ModelSerializer):
    serializer_related_field = FRelatedField
    idx = serializers.CharField(read_only=True)

    class Meta:
        fields = "__all__"
        # exclude = ["modified_on", "is_obsolete", 'obsolete_on']
        # extra_kwargs = {
        #     "created_on": {"read_only": True},
        #     "modified_on": {"read_only": True},
        #     "obsolete_on": {"read_only": True}
        # }


class CustomBaseSerializer(CustomValidationMessageForSerializerMixin, serializers.Serializer):
    pass
