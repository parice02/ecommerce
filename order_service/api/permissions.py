from rest_framework import permissions


class OrderReadWritePermission(permissions.BasePermission):
    """ """

    def has_permission(self, request, view):
        return True
