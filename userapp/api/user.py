from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from commonapp.models.company import Company, CompanyUser
from userapp.serializers.user import UserSerializer, UserDetailSerializer, UserRegistrationSerializer,\
    CompanyUserRegistrationSerializer, ChangePasswordSerializer, PasswordResetTokenSerializer,\
    ResetPasswordSerializer, GroupSerializer, UserGroupSerializer, SignupTokenSerializer, VerifyPasswordSerializer,\
    ChangeUserEmailSerializer, ChangeUserProfilePictureSerializer
from userapp.models.user import User, PasswordResetToken, LoginToken, SignupToken
from permission import isAdmin, isCompanyOwnerAndAllowAll, isCompanyManagerAndAllowAll

class GroupListView(generics.GenericAPIView):
    serializer_class = GroupSerializer
    permission_classes = (isAdmin, )

    def get(self, request):
        """
        An endpoint for listing all the groups.
        """
        group_obj = Group.objects.all()
        serializer = GroupSerializer(group_obj, many=True, context={'request':request})
        data = {
            'success': 1,
            'group': serializer.data
        }
        return Response(data, status=200)

class CompanyGroupListView(generics.GenericAPIView):
    serializer_class = GroupSerializer
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]

    def get(self, request):
        """
        An endpoint for listing all the groups associated with vendor.
        """
        company_group = ['owner', 'manager', 'sales']
        group_obj = Group.objects.filter(name__in=company_group)
        serializer = GroupSerializer(group_obj, many=True, context={'request':request})
        data = {
            'success': 1,
            'group': serializer.data
        }
        return Response(data, status=200)

class UserGroupDetailView(generics.GenericAPIView):
    permission_classes = [isCompanyOwnerAndAllowAll | isCompanyManagerAndAllowAll]
    serializer_class = UserGroupSerializer

    def get(self, request, company_id, user_id):
        """
        An endpoint for getting vendor user's group.
        """
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
        """
        An endpoint for changing vendor user's group.
        """
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

class UserListView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        """
        An endpoint for listing all the users. Pass 'page' and 'size' as query for requesting particular page and
        number of items per page respectively.
        """
        if request.user.admin:
            page_size = request.GET.get('size', 10)
            page_number = request.GET.get('page')
            user_obj = User.objects.all().order_by('-id')
            paginator = Paginator(user_obj, page_size)
            page_obj = paginator.get_page(page_number)
            serializer = UserSerializer(page_obj, many=True,\
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

class UpdateUser(generics.GenericAPIView):
    serializer_class = UserDetailSerializer

    def get(self, request, user_id):
        """
        An endpoint for getting user detail.
        """
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
        """
        An endpoint for updating detail.
        """
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
        """
        An endpoint for deleting user.
        """
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
    An endpoint for changing user's password.
    """
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
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
            # set_password also hashes the password that the user entered
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

class GeneratePasswordResetTokenView(generics.GenericAPIView):
    serializer_class = PasswordResetTokenSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        """
        An endpoint for generating password reset token.
        """
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
    An endpoint for resetting user's password.
    """
    serializer_class = ResetPasswordSerializer
    model = User
    permission_classes = (AllowAny, )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            # Check token exist
            token_obj = PasswordResetToken.objects.filter(token=serializer.data.get("token"), is_used=False)
            if not token_obj:
                data = {
                    'success': 0,
                    'message': "Invalid token.",
                }
                return Response(data, status=400)
            # set_password also hashes the password that the user entered
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

class CreateUserView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        """
        An endpoint for user registration as normal user or vendor.
        """
        serializer = UserRegistrationSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            if serializer.validated_data['password'] == serializer.validated_data['confirm_password']:
                user_obj = User.objects.create_user(
                    first_name=serializer.validated_data['first_name'],
                    middle_name=serializer.data.get('middle_name', ''),
                    last_name=serializer.validated_data['last_name'],
                    email=serializer.validated_data['email'],
                    phone_number=serializer.validated_data['phone_number'],
                    password=serializer.validated_data['password'],
                )
                if serializer.validated_data['is_user']:
                    group, _ = Group.objects.get_or_create(name='user')
                else:
                    group, _ = Group.objects.get_or_create(name='owner')

                user_obj.gender = serializer.validated_data['gender']
                user_obj.group = group
                user_obj.save()
                # generate JWT token for immediate login
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user_obj)
                token = jwt_encode_handler(payload)
                data = {
                    'success': 1,
                    'user': serializer.data,
                    'token': token
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

class CreateStaffUserView(generics.GenericAPIView):
    permission_classes = (isCompanyOwnerAndAllowAll, )
    serializer_class = CompanyUserRegistrationSerializer

    def post(self, request, company_id):
        """
        An endpoint for user registration as vendor's staff.
        """
        company_obj = Company.objects.filter(id=company_id)
        if company_obj:
            serializer = CompanyUserRegistrationSerializer(data=request.data, context={'request':request})
            if serializer.is_valid():
                if serializer.validated_data['password'] == serializer.validated_data['confirm_password']:
                    user_obj = User.objects.create_user(
                        first_name=serializer.validated_data['first_name'],
                        middle_name=serializer.data.get('middle_name', ''),
                        last_name=serializer.validated_data['last_name'],
                        gender=serializer.validated_data['gender'],
                        email=serializer.validated_data['email'],
                        phone_number=serializer.validated_data['phone_number'],
                        password=serializer.validated_data['password'],
                    )
                    if serializer.validated_data['is_manager']:
                        group, _ = Group.objects.get_or_create(name='manager')
                    else:
                        group, _ = Group.objects.get_or_create(name='sales')

                    user_obj.gender = serializer.validated_data['gender']
                    user_obj.group = group
                    user_obj.save()
                    CompanyUser.objects.create(user=user_obj, company=company_obj[0], is_staff=True)
                    # generate JWT token for immediate login
                    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                    payload = jwt_payload_handler(user_obj)
                    token = jwt_encode_handler(payload)
                    data = {
                        'success': 1,
                        'user': serializer.data,
                        'token': token
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

class SignupTokenView(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = SignupTokenSerializer

    def get(self, request):
        """
        An endpoint for verifying signup token. Pass 'email' and 'phone_number' as query.
        """
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
        """
        An endpoint for generating signup token.
        """
        user_obj = User.objects.filter(email=request.data['email'], phone_number=request.data['phone_number'])
        if user_obj:
            data = {
                'success': 0,
                'message': "User already exists."
            }
            return Response(data, status=400)
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

class VerifyUserPasswordView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = VerifyPasswordSerializer

    def post(self, request):
        """
        An endpoint for verifying user's password.
        """
        serializer = VerifyPasswordSerializer(request.data, context={'request': request})
        if request.user.check_password(serializer.data.get("password")):
            data = {
                'success': 1,
                'message': 'User password verified.'
            }
            return Response(data, status=200)
        else:
            data = {
                'success': 0,
                'message': 'User password not verified.'
            }
            return Response(data, status=400)

class ChangeUserEmailView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChangeUserEmailSerializer

    def put(self, request, user_id):
        """
        An endpoint for changing user's email.
        """
        if request.user.id == user_id:
            serializer = ChangeUserEmailSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                user = request.user
                if user.check_password(serializer.data.get("password")):
                    if user.email != serializer.data.get('email'):
                        if not User.objects.filter(email=serializer.data.get('email')):
                            user.email = serializer.data.get('email')
                            user.save()
                            data = {
                                'success': 1,
                                'email': serializer.data.get('email')
                            }
                            return Response(data, status=200)
                        else:
                            data = {
                                'success': 0,
                                'message': 'Email is already taken.'
                            }
                            return Response(data, status=400)
                    else:
                        data = {
                            'success': 0,
                            'message': 'Please enter new email.'
                        }
                        return Response(data, status=400)
                else:
                    data = {
                        'success': 0,
                        'message': 'User not verified.'
                    }
                    return Response(data, status=403)
            else:
                data = {
                    'success': 0,
                    'message': serializer.errors
                }
                return Response(data, status=400)
        else:
            data = {
                'success': 0,
                'message': "You don't have permission to update email."
            }
            return Response(data, status=403)

class ChangeUserProfilePictureView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChangeUserProfilePictureSerializer

    def put(self, request, user_id):
        """
        An endpoint for changing user's profile picture.
        """
        if request.user.id == user_id:
            serializer = ChangeUserProfilePictureSerializer(instance=request.user, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': 1,
                    'image': serializer.data
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
                'message': "You don't have permission to update profile."
            }
            return Response(data, status=403)