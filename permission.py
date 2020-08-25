from rest_framework import permissions

class isAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self,request,view):
        if request.method=='GET':
            return True
        return request.user and request.user.is_authenticated

# admin has access to all methods and api
class isAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.group.name == 'admin':
            return True
        return False

class isCompanyOwnerAndAllowAll(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.group.name == 'owner':
            return True
        return False

class isCompanyManagerAndAllowAll(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.group.name == 'manager':
            return True
        return False

class isCompanySalePerson(permissions.BasePermission):
    def has_permission(self, request, view):
        # if request.method=='GET':
        #     return True
        # else:
        if request.user.is_authenticated and request.user.group.name == 'sales':
            return True
        return False

class isUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method=='GET':
            return True
        if request.user.is_authenticated and request.user.group.name == 'user':
            return True
        return False