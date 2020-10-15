from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from commonapp.models.company import CompanyUser
from userapp.models.user import User, LoginToken
from userapp.serializers.login import LoginTokenSerializer, LoginJWTObtainSerializer
from userapp.serializers.user import UserDetailSerializer

class LoginTokenView(generics.GenericAPIView):
    serializer_class = LoginTokenSerializer
    permission_classes = (AllowAny, )

    def post(self, request, group):
        """
        An endpoint for getting login token. Send user, vendor and admin as path parameter for respective login.
        """
        group_name = {
            'admin': ['admin'],
            'vendor': ['owner', 'manager', 'sales'],
            'user': ['user']
        }
        user_obj = User.objects.filter(email=request.data['email'])
        if user_obj:
            if user_obj[0].check_password(request.data['password']):
                if user_obj[0].group.filter(name__in=group_name[group]).exists():
                    login_token_obj = LoginToken.objects.filter(user=user_obj[0].id, is_used=False)
                    # disable all login token of requesting user
                    for obj in login_token_obj:
                        obj.is_used = True
                        obj.save()
                    # create login token and send to user
                    login_token_obj = LoginToken.objects.create(user=user_obj[0])
                    data = {
                        'success': 1,
                        'data': None
                    }
                    return Response(data, status=200)
                else:
                    data = {
                        'success': 0,
                        'message': "Credential mismatch."
                    }
                    return Response(data, status=400)
            else:
                data = {
                    'success': 0,
                    'message': "Credential mismatch."
                }
                return Response(data, status=400)
        else:
            data = {
                    'success': 0,
                    'message': "User doesn't exist."
                }
            return Response(data, status=404)

class LoginJWTObtainView(generics.GenericAPIView):
    serializer_class = LoginJWTObtainSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        """
        An endpoint for getting user's detail and JWT token.
        """
        token = request.data['token']
        login_token_obj = LoginToken.objects.filter(token=token, is_used=False)
        if login_token_obj:
            login_token_obj[0].is_used = True
            login_token_obj[0].save()
            serializer = UserDetailSerializer(login_token_obj[0].user, context={'request':request})
            # create JWT token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(login_token_obj[0].user)
            token = jwt_encode_handler(payload)
            data = {
                'success': 1,
                'token': token,
                'user': serializer.data                
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Invalid login token."
            }
            return Response(data, status=400)
