from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminForNoSafeMethods(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            return request.user.is_authenticated and request.user.is_staff
        return True
