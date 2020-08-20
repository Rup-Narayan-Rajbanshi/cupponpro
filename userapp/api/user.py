from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from userapp.serializers.user import UserSerializer, UserDetailSerializer, ChangePasswordSerializer, PasswordResetTokenSerializer, ResetPasswordSerializer, GroupSerializer
from userapp.models.user import User, PasswordResetToken
from rest_framework.permissions import AllowAny
from permission import isAdmin

class GroupListView(APIView):
    serializer_class = GroupSerializer
    permission_classes = (isAdmin, )

    def get(self, request):
        group_obj = Group.objects.all()
        serializer = GroupSerializer(group_obj, many=True)
        data = {
            'success': 1,
            'group': serializer.data
        }
        return Response(data, status=200)

class UserListView(APIView):
    """
    An endpoint for get all user or create new user.
    """
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
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['password'] == serializer.validated_data['confirm_password']:
                user_obj = User.objects.create_user(
                    first_name=serializer.validated_data['first_name'],
                    middle_name=serializer.validated_data['middle_name'],
                    last_name=serializer.validated_data['last_name'],
                    email=serializer.validated_data['email'],
                    phone_number=serializer.validated_data['phone_number'],
                    password=serializer.validated_data['password']
                )
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

class UpdateUser(APIView):
    """
    An endpoint for get, update or delete user info.
    """
    serializer_class = UserDetailSerializer

    def get(self, request, user_id):
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

    def put(self, request, user_id):
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
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
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
    """
    An endpoint for generating password reset token.
    """
    serializer_class = PasswordResetTokenSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        if 'email' in request.data:
            user = User.objects.filter(email=request.data['email'])
        else:
            data = {
                'success': 0,
                'message': 'Enter email field'
            }
            return Response(data, status=400)
        if user:
            password_reset_token_obj = PasswordResetToken.objects.filter(user=user[0].id, is_used=False)
            for obj in password_reset_token_obj:
                obj.is_used = True
                obj.save()
            serializer = PasswordResetTokenSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'passwordresettoken': request.data['email']
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
    permission_classes = (AllowAny, )

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
            user = User.objects.get(id = token_obj[0].user.id)
            user.set_password(serializer.data.get("new_password"))
            user.save()
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

class LoginView(APIView):

    def get(self, request):
        user_type = request.user.group.name
        serializer = UserDetailSerializer(request.user)
        data = {
            'success': 1,
            'user_type': user_type,
            'user': serializer.data
        }
        return Response(data, status=200)