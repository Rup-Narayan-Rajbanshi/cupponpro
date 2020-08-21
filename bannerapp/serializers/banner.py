from bannerapp.models import Banner
from rest_framework import serializers


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = '__all__'


# class UpdateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'first_name', 'middle_name', 'last_name',\
#             'phone_number', 'email', 'group', 'active', 'admin', 'password',\
#             'confirm_password', 'image')
#         read_only_fields = ('image', 'active')
