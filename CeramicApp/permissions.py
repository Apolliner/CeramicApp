from rest_framework import permissions
from django.contrib.auth.models import Group


class NotePermission(permissions.BasePermission):
    """
        Разрешения доступа к модели Note
    """
    def has_object_permission(self, request, view, obj):
        """ 
            Углублённая проверка доступа

            User и Manager могут открывать и редактировать только свои заметки,
            Admin видит и может менять всё.
        """
        if request.user.level in ("User", "Manager"):
            if obj.autor == request.user:
                return True
        elif request.user.level == "Admin":
            return True
        return False


class OrganizationPermission(permissions.BasePermission):
    """
        Разрешения доступа к модели Organization

        Видеть, редактировать и создавать новые огранизации может только Admin
    """
    def has_permission(self, request, view):
        """ 
            Первоначальная проверка доступа
        """
        if request.user.level == "Admin":
            return True
        return False
    def has_object_permission(self, request, view, obj):
        """ 
            Углублённая проверка доступа
        """
        if request.user.level == "Admin":
            return True
        return False


class UserPermission(permissions.BasePermission):
    """
        Разрешения доступа к модели User

        Доступ имеет только Admin
    """
    def has_permission(self, request, view):
        """ 
            Первоначальная проверка доступа
        """
        if request.user.level == "Admin":
            return True
        return False

