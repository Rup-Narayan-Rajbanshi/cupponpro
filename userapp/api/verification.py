from rest_framework.decorators import (
    api_view,
    permission_classes,
    renderer_classes,
)
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from helpers.api_mixins import FAPIMixin
from rest_framework.viewsets import GenericViewSet, mixins
from userapp.models import User, OTPVerificationCode
from userapp.serializers.verifications import SendOTPSerializer, VerifyOTPSerializer, VerifyOTPTokenSerializer


class SendVerificationCodeAPI(FAPIMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = OTPVerificationCode.objects.all().order_by('-created_at')
    serializer_class = SendOTPSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = super().create(request, *args, **kwargs)
        data = {
            'token': serializer.data.get('token')
        }
        return Response(data=data, status=status.HTTP_201_CREATED)

class VerifyVerificationCodeAPI(FAPIMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = OTPVerificationCode.objects.all().order_by('-created_at')
    serializer_class = VerifyOTPSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = super().create(request, *args, **kwargs)
        # print(serializer.data.get('type'))
        data = {
            'token': serializer.data.get('token')
        }
        return Response(data=data, status=status.HTTP_200_OK)


@api_view(["POST"])
@renderer_classes([JSONRenderer])
@permission_classes((AllowAny,))
def verify_otp_token(request):
    serializer = VerifyOTPTokenSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    return Response({'detail': 'Token is valid.'}, status=status.HTTP_200_OK)
