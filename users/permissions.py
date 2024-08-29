from rest_framework import permissions

from users.models import User


class IsUser(permissions.BasePermission):
    """ Предоставляет доступ владельцу объекта. """
    def has_object_permission(self, request, view, obj):
        return request.user == obj
