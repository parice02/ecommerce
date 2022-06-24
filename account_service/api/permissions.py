from rest_framework import permissions


class UserReadWritePermission(permissions.BasePermission):
    """ """

    def has_permission(self, request, view):
        if request.method in ("GET", "DELETE"):
            return True
        elif request.method in ("POST", "PATCH", "PUT") and request.data:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id or request.user.is_staff


class AdminPermission(permissions.BasePermission):
    """ """

    def has_permission(self, request, view):
        return request.user.is_staff
