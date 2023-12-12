from rest_framework import permissions

def is_crew(req):
    return bool(req.user.groups.filter(name='Delivery crew').exists())

def is_manager(req):
    return bool(req.user.groups.filter(name='Manager').exists())

def is_customer(req):
    return not is_crew(req) and not is_manager(req) and not req.user.is_superuser

class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, req, view):
        return req.user.is_superuser or is_manager(req)
class IsCrew(permissions.BasePermission):
    def has_permission(self, req, view):
        return is_crew(req)

class IsManager(permissions.BasePermission):
    def has_permission(self, req, view):
        return is_manager(req)