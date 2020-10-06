from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from userapp.models.user import User, LoginToken
from userapp.serializers.login import LoginSerializer

class LoginTokenView(generics.GenericAPIView):
    serializer_class = LoginSerializer
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
                if user_obj[0].group.name in group_name[group]:
                    login_token_obj = LoginToken.objects.filter(user=user_obj[0].id, is_used=False)
                    # disable all login token of requesting user
                    for obj in login_token_obj:
                        obj.is_used = True
                        obj.save()
                    # create login token and send to user
                    login_token_obj = LoginToken.objects.create(user=user_obj[0])
                    data = {
                        'success': 1,
                        'token': 'Token has been sent.',
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
