from rest_framework import permissions
from commonapp.models.company import CompanyUser


class isAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self,request,view):
        if request.method=='GET':
            return True
        return request.user and request.user.is_authenticated

# admin has access to all methods and api
class isAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.group.filter(name='admin').exists():
            return True
        return False

class isCompanyOwnerAndAllowAll(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.group.filter(name='owner').exists():
            return True
        return False

class isCompanyManagerAndAllowAll(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.group.filter(name='manager').exists():
            return True
        return False

class isCompanySalePersonAndAllowAll(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.group.filter(name='sales').exists():
            return True
        return False

class isUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method=='GET':
            return True
        if request.user.is_authenticated and request.user.group.filter(name='user').exists():
            return True
        return False

class publicReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method=='GET':
            return True


class CompanyUserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            company_user = CompanyUser.objects.filter(user=request.user)
            if company_user.exists():
                request.company = company_user[0].company
                return True
        return False
