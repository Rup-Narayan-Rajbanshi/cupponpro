from django.db import transaction
from rest_framework import serializers

from helpers.exceptions import InvalidRequestException
from helpers.serializer_fields import FRelatedField
from helpers.serializer_mixins import CustomValidationMessageForSerializerMixin


class CustomModelSerializer(CustomValidationMessageForSerializerMixin, serializers.ModelSerializer):
    serializer_related_field = FRelatedField
    id = serializers.CharField(read_only=True)

    class Meta:
        fields = "__all__"
        # exclude = ["modified_at"]
        extra_kwargs = {
            "created_at": {"read_only": True},
            "modified_at": {"read_only": True}
        }


class CustomBaseSerializer(CustomValidationMessageForSerializerMixin, serializers.Serializer):
    pass
