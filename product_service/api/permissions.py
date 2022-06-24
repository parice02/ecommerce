from rest_framework import permissions


class ProductReadWritePermission(permissions.BasePermission):
    """ """

    def has_permission(self, request, view):
        return True
