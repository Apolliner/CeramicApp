from django.db import models
#from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.base_user import BaseUserManager
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
	en = "EN"
	ru = "RU"

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

    @property
    def token(self):
        """
        Позволяет нам получить токен пользователя, вызвав `user.token` вместо
        `user.generate_jwt_token().

        Декоратор `@property` выше делает это возможным.
        `token` называется «динамическим свойством ».
        """
        return self._generate_jwt_token()
    def _generate_jwt_token(self):
        """
        Создает веб-токен JSON, в котором хранится идентификатор
        этого пользователя и срок его действия
        составляет 60 дней в будущем.
        """
        dt = datetime.datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': 555 #int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token #.decode('utf-8')

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

