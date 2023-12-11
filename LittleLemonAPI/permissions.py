from rest_framework import permissions

class IsCrew(permissions.BasePermission):
    def has_permission(self, req, view):
        return bool(req.user.groups.filter(name='Delivery crew').exists())

class IsManager(permissions.BasePermission):
    def has_permission(self, req, view):
        return bool(req.user.groups.filter(name='Manager').exists())