from rest_framework import permissions

class ManagerPermission(permissions.BasePermission):
    def has_permission(self, req, view):
        return bool(req.user.groups.filter(name='Manager').exists())