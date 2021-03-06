# CeramicApp

Серверное приложение с token аутентификацией, реализующее функционал создания и просмотра заметок с многоязычными полями и тремя уровнями доступа: "User", "Manager", "Admin". 
User может изменять и просматривать детальную информацию своих созданных заметок. Manager дополнительно может просматривать заголовки заметок авторов своей организации.
Admin может видеть, изменять и создавать всё. Назначение уровней доступа выше "User" возможно только при регистрации администратором нового пользователя, или изменением имеющегося. Токен, использующийся для аутентификации, так же несёт в себе информацию об выбраном пользователем языке.

Ответы стандартизированы и выглядят следующим образом:
------------------------------------------------------
  "success": true,
  "status code": 200,
  "message": "Notes fetched successfully",
  "data": [
        {
            "id": 1,
            "header_ru": "Заголовок на Русском",
            "startdate": "2021-09-01T22:51:20.759553Z"
        }
    ]

Документация:
-------------
Подробная документация в формате OpenAPI представлена в файле __openapi-schema.yml__

_При запуске на сервере, заменить "localhost" на ip адрес сервера._

__localhost:8000/registration/__
Принимает поля "name", "phone_number", "password" и "organization". Поле "organization" принимает id выбраной организации.
Поддерживает методы: POST.

__localhost:8000/login/__
Принимает поля "phone_number", "password" и "language", возвращает "token". Поле "language" на данный момент принимает только два варианта языка "en" и "ru".
Поддерживает методы: POST.

_Следующие адреса доступны только при предаче в заголовке запроса Bearer token полученного при аутентификации:_

__localhost:8000/profile/__
Отображает профиль аутентифицированного с помощью token пользователя, позволяет изменять "name" и "password".
Поддерживает методы: GET, PUT.

__localhost:8000/note/__
Отображает список заголовков созданных пользователем заметок, позволяет создавать новые заметки. При аутентификации пользователем с уровнем доступа "manager", позволяет просматривать заголовки заметок, созданных членами организации.
При создании заметки, принимает поля "header_en", "header_ru", "text_en", "text_ru". При добавлении других подерживаемых языков, потребуется так же передавать поля header_<короткое название языка> и text_<короткое название языка>.
Поддерживает методы: GET, POST.

__localhost:8000/note/<id заметки>/__
Доступен только для создателя заметки или администратора. Отображает заголовок и текст заметки, позволяет редактировать поля и удалять заметку.
При редактировании заметки, принимает поля "header_en", "header_ru", "text_en", "text_ru".
Поддерживает методы: GET, PUT, DELETE.

_Следующие адреса доступны только аутентифицированным пользователям с уровнем доступа "Admin":_

__localhost:8000/user/__
Отображает список с детальной информацией обо всех пользователях, позволяет администраторам вручную создавать пользователей с нужным уровнем доступа.
При создании пользователя принимает поля "name", "phone_number", "password", "level" и "organization". Поле "level" принимает значения "User", "Manager", "Admin".
Поддерживает методы: GET, POST.

__localhost:8000/user/<id пользователя>/__
Позволяет просматривать и редактировать все поля выбраного пользователя.
При редактировании пользователя принимает поля "name", "phone_number", "password", "level" и "organization". Поле "level" принимает значения "User", "Manager", "Admin".
Поддерживает методы: GET, PUT.

__localhost:8000/organization/__
Позволяет просматривать список организаций, позволяет создавать новые организаци. При создании принимает поле "name".
Поддерживает методы: GET, POST.

__localhost:8000/organization/<id пользователя>/__
Позволяет просматривать и редактировать и удалять выбраную организацию. При редактировании принимает поле "name".
Поддерживает методы: GET, PUT, DELETE.


Инструкции по запуску сервиса:
==============================

Для разработки и теста:
-------------------------------------
0) __Опционально__ активация виртуального окружения __env/scripts/activate__
1) Установка зависимостей: __pip install -r requirements.txt__
2) Создание суперпользователя командой: __python manage.py createsuperuser__
3) Запуск сервера __python manage.py runserver__

Для работы в docker-compose:
----------------------------
1) Создание суперпользователя командой: __python manage.py createsuperuser__
2) Запуск докера командой: __docker-compose up --build__
