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


user_group, created = Group.objects.get_or_create(name='user')

manager_group, created = Group.objects.get_or_create(name='manager')

admin_group, created = Group.objects.get_or_create(name='admin')
permission_list = ['CeramicApp.add_Note',
                   'CeramicApp.change_Note',
                   'CeramicApp.delete_Note',
                   'CeramicApp.view_Note',
                   ]
#admin_group.permissions.add(permission_list)
