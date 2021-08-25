from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
#from django.contrib.auth.models import User

#from .managers import CustomUserManager

import datetime

class AccessLevel(models.TextChoices):
	user			= "User"
	manager			= "Manager"
	admin			= "Admin"

class LanguageChoice(models.TextChoices):
	en = "EN"
	ru = "RU"

class Organization(models.Model):
	name			= models.TextField("Название организации", max_length=100, blank=False, null=False)

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


class User(AbstractBaseUser,PermissionsMixin):
    name			= models.TextField("ФИО", max_length=100, blank=False, null=False)
    phone_number	= models.CharField("Телефон", max_length=11, blank=False, null=False, unique=True)
    password		= models.TextField("Пароль", max_length=100, blank=False, null=False)
    level			= models.CharField("Уровень доступа", max_length=7, choices=AccessLevel.choices, blank=False, null=False, default=AccessLevel.user)
    organization	= models.ForeignKey(Organization, on_delete=models.PROTECT, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


#class User(models.Model):
#	name			= models.TextField("ФИО", max_length=100, blank=False, null=False)
#	phone_number	= models.CharField("Телефон", max_length=8, blank=False, null=False, unique=True)
#	password		= models.TextField("Пароль", max_length=100, blank=False, null=False)
#	level			= models.CharField("Уровень доступа", max_length=7, choices=AccessLevel.choices, blank=False, null=False, default=AccessLevel.user)
#	organization	= models.ForeignKey(Organization, default="general", on_delete=models.PROTECT)

#class User(AbstractUser):
#	phone_number	= models.CharField("Телефон", max_length=8, blank=False, null=False, unique=True)
#	level			= models.CharField("Уровень доступа", max_length=7, choices=AccessLevel.choices, blank=False, null=False, default=AccessLevel.user)
#	organization	= models.ForeignKey(Organization, default="general", on_delete=models.PROTECT)
#	class Meta:
#		proxy = True


#class User(AbstractUser):
#	name			= models.TextField("ФИО", max_length=100, blank=False, null=False)
#	phone_number	= models.CharField(blank=False, max_length=11, unique=True)

#	USERNAME_FIELD	= phone_number
#	REQUIRED_FIELDS = []

#	objects = CustomUserManager()

#	level			= models.CharField("Уровень доступа", max_length=7, choices=AccessLevel.choices, blank=False, null=False, default=AccessLevel.user)
#	organization	= models.ForeignKey(Organization, default="general", on_delete=models.PROTECT)
    
#	def __str__(self):
#		return self.phone_number


class Language(models.Model):
	short_name		= models.TextField("Короткое название",choices=LanguageChoice.choices, max_length=2, blank=False, null=False)

class Session(models.Model):
	user			= models.ForeignKey(User, on_delete=models.PROTECT)
	language		= models.ForeignKey(Language, default="EN", on_delete=models.PROTECT)

class Note(models.Model):
	autor			= models.ForeignKey(User, on_delete=models.PROTECT)
	header			= models.TextField("Заголовок", max_length=100, blank=False, null=False)
	text			= models.TextField("Текст заметки", max_length=2000, blank=False, null=False)
	startdate		= models.DateTimeField("Дата публикации", blank=False, null=False, default=datetime.datetime.now)
