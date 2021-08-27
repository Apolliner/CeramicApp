from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
#from CeramicApp.models import AccessLevel
from django.db import models

class AccessLevel(models.TextChoices):
	user			= "User"
	manager			= "Manager"
	admin			= "Admin"

class UserManager(BaseUserManager):

    def create_user(self, name, phone_number, password=None,**kwargs):
        """
        Создание пользователя
        """
        if not name:
            raise ValueError('Users must have an name')
        if not phone_number:
            raise ValueError('Users must have an phone_number')

        user = self.model(name=name,
            phone_number=phone_number,**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_manager(self, name, phone_number, password=None,**kwargs):
        """
        Создание менеджера
        """
        if not name:
            raise ValueError('Users must have an name')
        if not phone_number:
            raise ValueError('Users must have an phone_number')
        user = self.model(name=name,
            phone_number=phone_number,**kwargs)

        user.set_password(password)
        user.level = AccessLevel.manager
        user.save(using=self._db)
        return user

    def create_superuser(self, name, phone_number, password):
        """
        Создание администратора
        """
        user = self.create_user(
            name,
            phone_number,
            password=password
        )
        user.is_superuser = True
        user.level = AccessLevel.admin
        user.save(using=self._db)
        return user
