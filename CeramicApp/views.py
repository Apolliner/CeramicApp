from rest_framework import renderers, viewsets, permissions, generics, status
from CeramicApp.models import AccessLevel, User, Organization, Language, Session, Note
from CeramicApp.serializers import UserSerializer, OrganizationSerializer, LanguageSerializer, SessionSerializer, UserRegistrationSerializer
from CeramicApp.serializers import NoteSerializer, ProfileSerializer, UpdateUserSerializer, UserLoginSerializer
from CeramicApp.permissions import NotePermission, OrganizationPermission, UserPermission
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.hashers import make_password

JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER

class Fictive_get_extra_actions:
    """ 
        Router требует наличия метода get_extra_actions. Наследование от этого класса решает эту проблему 
    """
    @classmethod
    def get_extra_actions(cls):
        """ Фиктивный метод для прохождения проверки роутером """
        return []

class AddCustomResponce:
    """ Класс для добавления метода кастомного ответа """
    def custom_response(self, success, status, message, error=None, token=None, data=None):
        """ Возвращает кастомный ответ """
        response = {
                    'success': success,
                    'status code': status,
                    'message': message,
                    }
        if error:
            response['error'] = error
        if token:
            response['token'] = token
        if data:
            response['data'] = data
        return Response(response, status=status)


class UserProfileView(APIView, AddCustomResponce):
    """ 
        Просмотр пользователем своего профиля 
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = ProfileSerializer

    def get(self, request):
        language = JWT_DECODE_HANDLER(request.headers['Authorization'][7:])['language']
        try:
            user_profile = User.objects.get(phone_number=request.user.phone_number)
            organization = None
            if user_profile.organization:
                organization = user_profile.organization.id
            data = [{
                    'name': user_profile.name,
                    'phone_number': user_profile.phone_number,
                    'level': user_profile.level,
                    'organization': organization,
                    'language': language,
                    }]
            return self.custom_response(True, status.HTTP_200_OK, 'User profile fetched successfully', data=data)
        except Exception:
            error = Exception
        return self.custom_response(False, status.HTTP_400_BAD_REQUEST, 'User does not exists', error=str(error))
    
    def put(self, request):
        """
            Изменение личных данных пользователя администратором
        """
        self.object = User.objects.get(phone_number=request.user.phone_number)
        serializer = UpdateUserSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data.get("name"):
                self.object.name = serializer.data.get("name")
            if serializer.data.get("password"):
                self.object.password = make_password(serializer.data.get("password"))
            self.object.save()
            return self.custom_response(True, status.HTTP_200_OK, 'The user update was successful')

        return self.custom_response(False, status.HTTP_400_BAD_REQUEST, 'The user update failed', error=str(serializer.errors))

class UserLoginView(APIView, Fictive_get_extra_actions, AddCustomResponce):
    """ 
        Аутентификация пользователя, возвращающая токен 
    """
    queryset = ''
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.custom_response(True, status.HTTP_200_OK, 'User logged in successfully', token=serializer.data['token'])


class UserRegistrationView(CreateAPIView, AddCustomResponce):
    """ Регистрация пользователя """
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.custom_response(True, status.HTTP_201_CREATED, 'User registered successfully')


class NoteViewSet(viewsets.ModelViewSet, AddCustomResponce):
    """ 
        Обработка обращений к модели Note 
    """
    permission_classes = [NotePermission]
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_use_serializer(self, language, text=False):
        """ 
            Возвращает сериализатор с отображением полей на языке language 
        """
        class AssembledNoteSerializer(self.serializer_class):
            class Meta:
                model = Note
                read_only_fields = ['id', 'autor', 'startdate']
                extra_kwargs = {
                                'header': {'source': 'header_en'},
                                'text': {'source': 'text_en'}
                                }
        serializer = AssembledNoteSerializer
        serializer.Meta.fields = ['id', 'autor', 'startdate']
        serializer.Meta.fields.append('header_' + str(language))
        if text:
            serializer.Meta.fields.append('text_' + str(language))
        return serializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.custom_response(True, status.HTTP_201_CREATED, 'Note created successfully')

    def list(self, request):
        """ 
            Отображение множества записей 
        """
        language = JWT_DECODE_HANDLER(request.headers['Authorization'][7:])['language']
        if request.user.level == 'User':
            use_serializer = self.get_use_serializer(language)
            notes = Note.objects.filter(autor=request.user.id)
        elif request.user.level == 'Manager':
            use_serializer = self.get_use_serializer(language)
            organization_members = User.objects.filter(organization=request.user.organization)
            organization_id = []
            for member in organization_members:
                organization_id.append(member.id)
            notes = Note.objects.filter(autor__in=organization_id)
            if not notes:
                return self.custom_response(True, status.HTTP_204_NO_CONTENT, 'No notes created')
        elif request.user.level == 'Admin':
            use_serializer = self.serializer_class
            notes = Note.objects.all()
        else:
            return self.custom_response(False, status.HTTP_400_BAD_REQUEST, 'Note does not exists')
        #Если всё прошло успешно
        serializer = use_serializer(instance=notes, many=True)
        return self.custom_response(True, status.HTTP_200_OK, 'Notes fetched successfully', data=serializer.data)

    def retrieve(self, request, pk=None):
        """ 
            Отображение одной записи 
        """
        if request.user.level == 'Admin':
            #Отображение всех полей для администратора
            use_serializer = self.serializer_class
        else:
            language = JWT_DECODE_HANDLER(request.headers['Authorization'][7:])['language']
            use_serializer = self.get_use_serializer(language, text=True)
        try:
            notes = Note.objects.filter(id=pk)
            serializer = use_serializer(instance=notes, many=True)
            self.check_object_permissions(request, notes[0])
            return self.custom_response(True, status.HTTP_200_OK, 'Note fetched successfully', data=serializer.data[0])
        except Exception:
            error = Exception
        return self.custom_response(False, status.HTTP_400_BAD_REQUEST, f'Note {pk} does not exists', error=str(error))


class UserViewSet(viewsets.ModelViewSet, AddCustomResponce):
    """
    Отображение списка пользователей для администратора.
    Администратор может видеть все данные всех пользователей и изменять их.
    """
    permission_classes = (UserPermission,) 
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        """ Отображение множества записей """
        try:
            users = User.objects.all()
            serializer = self.serializer_class(instance=users, many=True)
            return self.custom_response(True, status.HTTP_200_OK, 'Organizations fetched successfully', data=serializer.data)
        except Exception:
            error = Exception
        return self.custom_response(False, status.HTTP_400_BAD_REQUEST, f'Organizations does not exists', error=str(error))

    def retrieve(self, request, pk=None):
        """ 
            Отображение одной записи 
        """
        use_serializer = self.serializer_class
        try:
            user = User.objects.filter(id=pk)
            serializer = use_serializer(instance=user, many=True)
            self.check_object_permissions(request, user[0])
            return self.custom_response(True, status.HTTP_200_OK, 'User fetched successfully', data=serializer.data[0])
        except Exception:
            error = Exception
        return self.custom_response(False, status.HTTP_400_BAD_REQUEST, f'Note {pk} does not exists', error=str(error))

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, pk):
        """
            Изменение личных данных пользователя администратором
        """
        self.object = User.objects.filter(id=pk)[0]
        serializer = UpdateUserSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data.get("name"):
                self.object.name = serializer.data.get("name")
            if serializer.data.get("phone_number"):
                self.object.phone_number = serializer.data.get("phone_number")
            if serializer.data.get("level"):
                self.object.level = serializer.data.get("level")
            if serializer.data.get("organization"):
                organization = Organization.objects.filter(id=int(serializer.data.get("organization")))[0]
                self.object.organization = organization
            if serializer.data.get("password"):
                self.object.password = make_password(serializer.data.get("password"))
            self.object.save()
            return self.retrieve(request, pk)

        return self.custom_response(False, status.HTTP_400_BAD_REQUEST, 'The users change was unsuccessful', error=str(serializer.errors))

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.filter(phone_number=serializer.data.get("phone_number"))[0]
        if request.data["organization"]:
            organization = Organization.objects.filter(id=int(request.data["organization"]))[0]
            user.organization = organization
            user.save()
        return self.custom_response(True, status.HTTP_201_CREATED, 'User registered successfully')

    def perform_create(self, serializer):
        return super(UserViewSet, self).perform_create(serializer)


class OrganizationViewSet(viewsets.ModelViewSet, AddCustomResponce):
    permission_classes = (OrganizationPermission,) 
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.custom_response(True, status.HTTP_201_CREATED, 'Organization created successfully')

    def list(self, request):
        """ Отображение множества записей """
        try:
            organization = Organization.objects.all()
            serializer = self.serializer_class(instance=organization, many=True)
            return self.custom_response(True, status.HTTP_200_OK, 'Organizations fetched successfully', data=serializer.data)
        except Exception:
            error = Exception
        return self.custom_response(False, status.HTTP_400_BAD_REQUEST, f'Organizations does not exists', error=str(error))

    def retrieve(self, request, pk=None):
        """ Отображение одной записи """
        use_serializer = self.serializer_class
        try:
            organization = Organization.objects.filter(id=pk)
            serializer = use_serializer(instance=organization[0])
            return self.custom_response(True, status.HTTP_200_OK, 'Organizations fetched successfully', data=serializer.data)
        except Exception:
            error = Exception
        return self.custom_response(False, status.HTTP_400_BAD_REQUEST, f'Organizations does not exists', error=str(error))

    def update(self, request, pk=None):
        """ Отображение одной записи """
        use_serializer = self.serializer_class
        try:
            organization = Organization.objects.filter(id=pk)[0]
            serializer = use_serializer(data=request.data)
            if serializer.is_valid():
                organization.name = serializer.data.get("name")
                organization.save()
                return self.custom_response(True, status.HTTP_200_OK, 'Organizations update successfully')
        except Exception:
            error = Exception
        return self.custom_response(False, status.HTTP_400_BAD_REQUEST, f'Organizations does not exists', error=str(error))

    def perform_create(self, serializer):
        return super(OrganizationViewSet, self).perform_create(serializer)

class LanguageViewSet(viewsets.ModelViewSet, AddCustomResponce):
    permission_classes = (OrganizationPermission,) 
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    def perform_create(self, serializer):
        return super(LanguageViewSet, self).perform_create(serializer)