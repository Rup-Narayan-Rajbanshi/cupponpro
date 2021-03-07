from rest_framework.decorators import (
    api_view,
    permission_classes,
    renderer_classes,
)
from rest_framework_jwt.settings import api_settings
from userapp.models.user import SocialAccount
from userapp.serializers.user import UserDetailSerializer 
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
        if serializer.data.get('type') == 'SOCIAL_LOGIN':
            email = serializer.data.get('email')
            phone_number = serializer.data.get('phone_number')
            print(serializer.data)
            account = SocialAccount.objects.filter(email=email).first()
            if account:
                account.update(phone_number=phone_number)
                data = {'email':email, 'account_id': account.account_id, 'account_type': account.account_type,
                            'first_name':account.first_name, 'middle_name':account.middle_name, 'last_name':account.last_name,
                            'phone_number':phone_number}
                account = SocialAccount.create_user_account(**data)
                if account.user:
                    user = UserDetailSerializer(instance = account.user, context={'request':request})
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(account.user)
                    token = jwt_encode_handler(payload)
                    data = {
                        'success': 1,
                        'token': token,
                        'user': user.data,
                        'social_account': account.id
                    }
                else:
                    data = {
                        'success': 0,
                        'token': None,
                        'user': None,
                        'social_account': account.id
                    }
            else:
                data={
                    'success': 0,
                    'message': 'Social account do not exist'
                }
        else:
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
