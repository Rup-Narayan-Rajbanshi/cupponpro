from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from userapp.serializers.user import UserSerializer
from userapp.models import User



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
