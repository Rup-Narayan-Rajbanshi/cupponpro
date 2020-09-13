from django.contrib.auth.models import Group
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from commonapp.models.company import Company, CompanyUser
from userapp.serializers.user import UserSerializer, UserDetailSerializer, UserRegistrationSerializer,\
    CompanyUserRegistrationSerializer, ChangePasswordSerializer, PasswordResetTokenSerializer,\
    ResetPasswordSerializer, GroupSerializer, UserGroupSerializer, LoginTokenSerializer, LoginSerializer,\
    SignupTokenSerializer
from userapp.models.user import User, PasswordResetToken, LoginToken, SignupToken
from permission import isAdmin, isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll

class GroupListView(APIView):
    serializer_class = GroupSerializer
    permission_classes = (isAdmin, )

    def get(self, request):
        group_obj = Group.objects.all()
        serializer = GroupSerializer(group_obj, many=True, context={'request':request})
        data = {
            'success': 1,
            'group': serializer.data
        }
        return Response(data, status=200)

class CompanyGroupListView(APIView):
    serializer_class = GroupSerializer
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]

    def get(self, request):
        company_group = ['owner', 'manager', 'sales']
        group_obj = Group.objects.filter(name__in=company_group)
        serializer = GroupSerializer(group_obj, many=True, context={'request':request})
        data = {
            'success': 1,
            'group': serializer.data
        }
        return Response(data, status=200)

class UserGroupDetailView(APIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = UserGroupSerializer

    def get(self, request, company_id, user_id):
        company_user_obj = CompanyUser.objects.filter(user=user_id, company=company_id)
        if company_user_obj:
            user_obj = User.objects.filter(id=user_id)
            serializer = UserGroupSerializer(user_obj[0], context={'request':request})
            data = {
                'success': 1,
                'group': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 1,
                'message': "User doesn't exist."
            }
            return Response(data, status=404)
    
    def put(self, request, company_id, user_id):
        group_modify_access = {'owner': ['manager', 'sales'], 'manager': ['sales']}
        group_name = Group.objects.get(id=request.data['group']).name
        if group_name in group_modify_access[request.user.group.name]:
            company_user_obj = CompanyUser.objects.filter(user=user_id, company=company_id)
            if company_user_obj:
                user_obj = User.objects.filter(id=user_id)
                serializer = UserGroupSerializer(instance=user_obj[0], data=request.data, context={'request':request})
                if serializer.is_valid():
                    serializer.save()
                    data = {
                        'success': 1,
                        'group': serializer.data
                    }
                    return Response(data, status=200)
                else:
                    data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)
            else:
                data = {
                    'success': 0,
                    'message': "User doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success': 0,
                'message': "Group change failed."
            }
            return Response(data, status=400)     

class UserListView(APIView):
    """
    An endpoint for getting all user or create new user.
    """
    serializer_class = UserSerializer

    def get(self, request):
        if request.user.admin:
            user_obj = User.objects.all().order_by('-id')
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
            'message': "User doesn't exist."
        }
        return Response(data, status=404)

    def put(self, request, user_id):
        if User.objects.filter(id=user_id):
            user_obj = User.objects.get(id=user_id)
            serializer = UserSerializer(instance=user_obj,\
                data=request.data, partial=True, context={'request':request})
            if 'image' in request.data and not request.data['image']:
                serializer.exclude_fields(['image'])
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
            'message': "User doesn't exist."
        }
        return Response(data, status=404)

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
                'message': "User doesn't exist."
            }
            return Response(data, status=404)
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
        serializer = self.get_serializer(data=request.data, context={'request':request})

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
                'message': 'Enter email field.'
            }
            return Response(data, status=400)
        if user:
            password_reset_token_obj = PasswordResetToken.objects.filter(user=user[0].id, is_used=False)
            for obj in password_reset_token_obj:
                obj.is_used = True
                obj.save()
            serializer = PasswordResetTokenSerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'password_reset_token': "Password reset token sent."
                }
                return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "Email doesn't exist."
            }
            return Response(data, status=404)

class ResetPasswordView(generics.UpdateAPIView):
    """
    An endpoint for resetting password.
    """
    serializer_class = ResetPasswordSerializer
    model = User
    permission_classes = (AllowAny, )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            # Check token exist
            token_obj = PasswordResetToken.objects.filter(token=serializer.data.get("token"), user=request.user.id, is_used=False)
            if not token_obj:
                data = {
                    'success': 0,
                    'message': "Invalid token.",
                }
                return Response(data, status=400)
            # set_password also hashes the password that the user will get
            user = User.objects.get(id=token_obj[0].user.id)
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

class CreateUserView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            if serializer.validated_data['password'] == serializer.validated_data['confirm_password']:
                user_obj = User.objects.create_user(
                    first_name=serializer.validated_data['first_name'],
                    middle_name=serializer.validated_data['middle_name'],
                    last_name=serializer.validated_data['last_name'],
                    email=serializer.validated_data['email'],
                    phone_number=serializer.validated_data['phone_number'],
                    password=serializer.validated_data['password'],
                )
                if serializer.validated_data['is_user']:
                    group, created = Group.objects.get_or_create(name='user')
                else:
                    group, created = Group.objects.get_or_create(name='owner')

                user_obj.group = group
                user_obj.save()
                data = {
                    'success': 1,
                    'user': serializer.data
                }
                return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    'message': 'Password do not match.'
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': serializer.errors
            }
            return Response(data, status=400)

class CreateStaffUserView(APIView):
    permission_classes = (isCompanyOwnerAndAllowAll, )
    serializer_class = CompanyUserRegistrationSerializer

    def post(self, request, company_id):
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            serializer = CompanyUserRegistrationSerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                if serializer.validated_data['password'] == serializer.validated_data['confirm_password']:
                    user_obj = User.objects.create_user(
                        first_name=serializer.validated_data['first_name'],
                        middle_name=serializer.validated_data['middle_name'],
                        last_name=serializer.validated_data['last_name'],
                        email=serializer.validated_data['email'],
                        phone_number=serializer.validated_data['phone_number'],
                        password=serializer.validated_data['password'],
                    )
                    if serializer.validated_data['is_manager']:
                        group, created = Group.objects.get_or_create(name='manager')
                    else:
                        group, created = Group.objects.get_or_create(name='sales')

                    user_obj.group = group
                    user_obj.save()
                    CompanyUser.objects.create(user=user_obj, company=company_obj[0], is_staff=True)
                    data = {
                        'success': 1,
                        'user': serializer.data
                    }
                    return Response(data, status=200)
                else:
                    data = {
                        'success': 0,
                        'message': 'Password do not match.'
                    }
                    return Response(data, status=400)
            else:
                data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "Company doesn't exist."
            }
            return Response(data, status=404)

class GenerateLoginTokenView(APIView):
    """
    An endpoint for generating login token.
    """
    serializer_class = LoginTokenSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        if 'email' in request.data:
            user = User.objects.filter(email=request.data['email'])
        else:
            data = {
                'success': 0,
                'message': 'Enter email field.'
            }
            return Response(data, status=400)
        if user:
            login_token_obj = LoginToken.objects.filter(user=user[0].id, is_used=False)
            for obj in login_token_obj:
                obj.is_used = True
                obj.save()
            serializer = LoginTokenSerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'login_token': "Login token sent."
                }
                return Response(data, status=200)
            data = {
                'success': 0,
                'message': serializer.errors
            }
            return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "Email doesn't exist."
            }
            return Response(data, status=404)

class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        token = request.data['token']
        login_token_obj = LoginToken.objects.filter(token=token, user=request.user.id, is_used=False)
        if login_token_obj:
            login_token_obj[0].is_used = True
            login_token_obj[0].save()
            serializer = UserDetailSerializer(request.user, context={'request':request})
            data = {
                'success': 1,
                'user_type': request.user.group.name,
                'user': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': "Invalid login token."
            }
            return Response(data, status=400)

class SignupTokenView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = SignupTokenSerializer

    def get(self, request):
        email = request.GET.get('email', None)
        phone_number = request.GET.get('phone_number', None)
        if email and phone_number:
            token_obj = SignupToken.objects.filter(email=email, phone_number=phone_number, is_used=False)
            if token_obj:
                token_obj[0].is_used = True
                token_obj[0].save()
                serializer = SignupTokenSerializer(token_obj[0], context={'request':request})
                data = {
                    'success': 1,
                    'signup_token': serializer.data
                }
                return Response(data, status=200)
            else:
                data = {
                    'success': 0,
                    'message': "Signup token doesn't exist."
                }
                return Response(data, status=404)
        else:
            data = {
                'success': 0,
                'message': "Please pass email and phone number as get request"
            }
            return Response(data, status=400)



    def post(self, request):
        token_obj = SignupToken.objects.filter(email=request.data['email'], phone_number=request.data['phone_number'])
        if token_obj:
            for obj in token_obj:
                obj.is_used = True
                obj.save()
        serializer = SignupTokenSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            data = {
                'success': 1,
                'signup_token': serializer.data
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': serializer.errors
            }
            return Response(data, status=400)
