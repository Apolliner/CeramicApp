from rest_framework import permissions
from django.contrib.auth.models import Group

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner.
        return True #obj.owner == request.user

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

        Редактировать и создавать новые огранизации может только Admin
    """
    def has_permission(self, request, view):
        """ 
            Первоначальная проверка доступа
        """
        if request.user.level in ("User", "Manager"):
            if request.method in permissions.SAFE_METHODS:
                return True
        elif request.user.level == "Admin":
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


    



user_group, created = Group.objects.get_or_create(name='user')

manager_group, created = Group.objects.get_or_create(name='manager')

admin_group, created = Group.objects.get_or_create(name='admin')
permission_list = ['CeramicApp.add_Note',
                   'CeramicApp.change_Note',
                   'CeramicApp.delete_Note',
                   'CeramicApp.view_Note',
                   ]
#admin_group.permissions.add(permission_list)
