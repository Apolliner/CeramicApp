from django.db import models
from django.contrib.auth.models import User
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

#class User(models.Model):
#	name			= models.TextField("ФИО", max_length=100, blank=False, null=False)
#	phone_number	= models.CharField("Телефон", max_length=8, blank=False, null=False, unique=True)
#	password		= models.TextField("Пароль", max_length=100, blank=False, null=False)
#	level			= models.CharField("Уровень доступа", max_length=7, choices=AccessLevel.choices, blank=False, null=False, default=AccessLevel.user)
#	organization	= models.ForeignKey(Organization, default="general", on_delete=models.PROTECT)

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
