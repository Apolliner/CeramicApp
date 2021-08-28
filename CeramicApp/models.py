from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from CeramicApp.managers import UserManager
import datetime
from datetime import timedelta
import jwt
from django.conf import settings

class AccessLevel(models.TextChoices):
	user			= "User"
	manager			= "Manager"
	admin			= "Admin"

class LanguageChoice(models.TextChoices):
	en = "en"
	ru = "ru"

class Organization(models.Model):
    name			= models.TextField("Название организации", max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

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


Language.objects.create(short_name=LanguageChoice.en)
Language.objects.create(short_name=LanguageChoice.ru)