from rest_framework import permissions

def is_crew(req):
    return bool(req.user.groups.filter(name='Delivery crew').exists())

def is_manager(req):
    return bool(req.user.groups.filter(name='Manager').exists())

class IsCrew(permissions.BasePermission):
    def has_permission(self, req, view):
        return is_crew(req)

class IsManager(permissions.BasePermission):
    def has_permission(self, req, view):
        return is_manager(req)