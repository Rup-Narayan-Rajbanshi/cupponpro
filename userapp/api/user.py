from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from userapp.serializers.user import UserSerializer, ChangePasswordSerializer, PasswordResetTokenSerializer, ResetPasswordSerializer
from userapp.models.user import User, PasswordResetToken
from rest_framework.permissions import IsAuthenticated
from permission import PasswordResetPermission



class UserListView(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        if request.user.admin:
            user_obj = User.objects.all()
            serializer = UserSerializer(user_obj, many=True,\
                context={"request": request})
            data = {
                'success': 1,
                'user': serializer.data,
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': "You do not have permission to list an user."
        }
        return Response(data, status=403)

    def post(self, request):
        if request.user.admin:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                if serializer.validated_data['password'] == serializer.validated_data['confirm_password']:
                    user_obj = User()
                    user_obj.first_name = serializer.validated_data['first_name']
                    user_obj.middle_name = serializer.validated_data['middle_name']
                    user_obj.last_name = serializer.validated_data['last_name']
                    user_obj.email = serializer.validated_data['email']
                    user_obj.phone_number = serializer.validated_data['phone_number']
                    user_obj.save()
                    data = {
                        'success': 1,
                        'user': serializer.data
                    }
                    return Response(data, status=200)
                data = {
                    'success': 0,
                    'message': 'Password do not match.'
                }
                return Response(data, status=400)
            data = {
                'success': 0,
                'message': serializer.errors
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': 'You do not have permission to add an user.'
        }
        return Response(data, status=403)



class UpdateUser(APIView):
    serializer_class = UserSerializer

    def get(self, request, user_id):
        if request.user.admin:
            if User.objects.filter(id=user_id):
                user_obj = User.objects.get(id=user_id)
                serializer = UserSerializer(user_obj,\
                    context={'request': request})
                data = {
                    'success': 1,
                    'user': serializer.data
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': 'User id not found.'
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': 'You do not have permission to show user.'
        }
        return Response(data, status=403)

    def put(self, request, user_id):
        if request.user.admin:
            if User.objects.filter(id=user_id):
                user_obj = User.objects.get(id=user_id)
                serializer = UserSerializer(instance=user_obj,\
                    data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        'success': 1,
                        'user': serializer.data
                    }
                    return Response(data, status=200)
                data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)
            data = {
                'success': 0,
                'message': 'User id not found.'
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': 'You do not have permission to update user.'
        }
        return Response(data, status=403)

    def delete(self, request, user_id):
        if request.user.admin:
            if User.objects.filter(id=user_id):
                user_obj = User.objects.get(id=user_id)
                user_obj.delete()
                data = {
                    'success': 1,
                    'user': 'User deleted successfully.'
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': 'User id not found.'
            }
            return Response(data, status=400)
        data = {
            'success': 0,
            'message': 'You do not have permission to delete user.'
        }
        return Response(data, status=403)

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                data = {
                    'success': 0,
                    'message': "Old password is not correct.",
                }
                return Response(data, status=400)
            # set_password also hashes the password that the user will get
            # self.object.set_password(serializer.data.get("new_password"))
            self.object.save_password(serializer.data.get("new_password"))
            print(self.object.check_password(serializer.data.get("new_password")))
            data = {
                'success': 1,
                'message': "Password changed successfully.",
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': serializer.errors,
        }
        return Response(data, status=400)

class GeneratePasswordResetTokenView(APIView):
    serializer_class = PasswordResetTokenSerializer

    def get(self, request):
        if 'email' in request.data:
            user = User.objects.filter(email=request.data['email'])
            if user:
                data = {
                        'success': 1,
                        'user': 'User exist.'
                    }
                status = 200
            else:
                data = {
                        'success': 0,
                        'message': 'User doesn\'t exist.'
                    }
                status = 400
            return Response(data, status)
        data = {
            'success': 0,
            'message': 'Enter email.'
        }
        return Response(data, status=400)

    def post(self, request):
        user = User.objects.filter(email=request.data['email'])
        if user:
            password_reset_token_obj = PasswordResetToken.objects.filter(email=request.data['email'], is_used=False)
            for obj in password_reset_token_obj:
                obj.is_used = True
                obj.save()
            serializer = PasswordResetTokenSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'passwordresettoken': serializer.data
                }
                return Response(data, status = 200)
            data = {
                'success': 0,
                'message': serializer.errors
            }
            return Response(data, status = 400)
        data = {
                'success': 0,
                'message': 'Email not found.'
            }
        return Response(data, status = 400)

class ResetPasswordView(generics.UpdateAPIView):
    """
    An endpoint for resetting password.
    """
    serializer_class = ResetPasswordSerializer
    model = User
    permission_classes = (PasswordResetPermission, )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check token exist
            token_obj = PasswordResetToken.objects.filter(token=serializer.data.get("token"), is_used=False)
            if not token_obj:
                data = {
                    'success': 0,
                    'message': "Invalid token.",
                }
                return Response(data, status=400)
            # set_password also hashes the password that the user will get
            user = User.objects.filter(email = token_obj[0].email)
            user = user[0]
            # user.set_password(serializer.data.get("new_password"))
            user.save_password(serializer.data.get("new_password"))
            token_obj[0].is_used = True
            token_obj[0].save()
            data = {
                'success': 1,
                'message': "Password reset successfully.",
            }
            return Response(data, status=200)
        data = {
            'success': 0,
            'message': serializer.errors,
        }
        return Response(data, status=400)