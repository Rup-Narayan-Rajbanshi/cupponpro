from rest_framework.permissions import AllowAny
from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework.viewsets import GenericViewSet
from helpers.api_mixins import FAPIMixin
from userapp.models import User
from userapp.serializers.registration import (
    UserRegisterSerializer
)


class UserRegisterAPI(FAPIMixin, mixins.CreateModelMixin, GenericViewSet):
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = super().create(request, *args, **kwargs)
        phone_number = serializer.data.get('phone_number')
        # generate JWT token for immediate login
        user_obj = User.objects.get(phone_number=phone_number)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)
        data = {
            'success': 1,
            'data': serializer.data,
            'token': token
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
