from rest_framework import serializers
from helpers.serializer import CustomModelSerializer
from company.models.follow import Follows
from helpers.serializer_fields import DetailRelatedField
from userapp.models.user import User
from commonapp.models.company import Company
from rest_framework.exceptions import ValidationError


class FollowSerializer(CustomModelSerializer):
    user = DetailRelatedField(model=User, lookup='id', representation='to_representation', required=False)
    company = DetailRelatedField(model=Company, lookup='id', representation='to_representation', required=True)

    class Meta:
        model = Follows
        fields = '__all__'

    def validate(self ,attrs):
        request = self.context['request']
        if request:
            attrs['user'] = request.user
            if Follows.objects.filter(user=request.user, company=attrs['company']).exists():
                raise ValidationError({'detail':'user has already followed the company'})
        return attrs