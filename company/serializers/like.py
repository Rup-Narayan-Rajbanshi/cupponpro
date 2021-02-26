from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from helpers.serializer import CustomModelSerializer, CustomBaseSerializer
from helpers.serializer_fields import DetailRelatedField
from company.models.likes import  Like
from userapp.models import User
from commonapp.models.company import Company


class LikeSerializer(CustomModelSerializer):
    company = DetailRelatedField(model=Company, lookup='id', representation='to_representation')
    user = DetailRelatedField(model=User, lookup='id', representation='to_representation')


    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        company = attrs['company']
        user = attrs['user']
        like_exists=Like.objects.filter(user=user,company=company).exists()
        if like_exists:
            raise ValidationError({'message': 'User has already liked this company'})
        
        return super().validate(attrs)

