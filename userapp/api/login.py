from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from userapp.models.user import User, LoginToken
from userapp.serializers.user import UserDetailSerializer
from userapp.serializers.login import LoginJWTTokenSerializer

class LoginJWTToken(generics.GenericAPIView):
    serializer_class = LoginJWTTokenSerializer

    def post(self, request):
        """
        An endpoint for login using JWT.
        """
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        user_obj = User.objects.filter(email=request.POST['email'])
        if user_obj:
            if user_obj[0].check_password(request.POST['password']):
                if user_obj[0].group.name == request.POST['group']:
                    payload = jwt_payload_handler(user_obj[0])
                    token = jwt_encode_handler(payload)
                    serializer = UserDetailSerializer(user_obj[0], context={'request':request})
                    login_token_obj = LoginToken.objects.filter(user=request.user.id, is_used=False)
                    # disable all login token of requesting user
                    for obj in login_token_obj:
                        obj.is_used = True
                        obj.save()
                    # create login token and send to user
                    login_token_obj = LoginToken.objects.create(user=request.user)
                    data = {
                        'success': 1,
                        'token': token,
                        'user_type': user_obj[0].group.name,
                        'user': serializer.data
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
