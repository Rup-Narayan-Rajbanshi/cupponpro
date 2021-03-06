from rest_framework import permissions

from company.models.asset import Asset
from company.models.company import CompanyUser, Company


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
        if request.method == 'GET':
            return True
        if request.user.is_authenticated and request.user.group.filter(name='user').exists():
            try:
                company_id = request.parser_context.get('kwargs')['company_id']
                request.company = Company.objects.get(id=company_id)
                return True
            except Exception as e:
                pass
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


class CompanyCustomerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            asset = Asset.objects.filter(id=request.GET.get('asset')).first()
            if asset and not request.user.is_authenticated:
                request.company = asset.company
                request.user = asset.company.get_or_create_company_customer_user()
        except:
            return False
        return False


class MasterQRUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if not request.user.is_authenticated:
            try:
                company_id = request.parser_context.get('kwargs')['company_id']
                company = Company.objects.get(id=company_id)
                request.user = company.qr_user
                request.company = company
                return True
            except Exception as e:
                pass
        return False
