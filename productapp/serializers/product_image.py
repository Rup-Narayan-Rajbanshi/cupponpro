from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from helpers.serializer_fields import ImageFieldWithURL
from django.contrib.contenttypes.models import ContentType
from commonapp.models.image import Image
from company.models.company import CompanyUser


class ImageSerializer(serializers.ModelSerializer):
    image = ImageFieldWithURL(allow_empty_file=False)
    content_type = serializers.SerializerMethodField()
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = '__all__'

    def validate(self, attrs):
        content_type = ContentType.objects.get(model='product')
        attrs['content_type'] = content_type
        object_id = attrs.get('object_id')
        content_class = content_type.model_class()
        user = self.context.get('request').user
        try:
            company_user = CompanyUser.objects.select_related('company').get(user=user)
            object = content_class.objects.get(id=object_id, company=company_user.company)
        except ObjectDoesNotExist:
            raise ValidationError({'object_id': 'Object does not exist.'})
        return attrs

    def get_content_object(self, obj):
        content_object = None
        if obj.content_object:
            content_object = obj.content_object.to_representation()
        return content_object

    def get_content_type(self, obj):
        content_type = obj.content_type.name
        return content_type
