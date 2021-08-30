from rest_framework import renderers, viewsets, permissions, generics, status
from CeramicApp.models import AccessLevel, User, Organization, Language, Session, Note
from CeramicApp.serializers import UserSerializer, OrganizationSerializer, LanguageSerializer, SessionSerializer, NoteSerializer
from CeramicApp.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from CeramicApp.serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER

class Fictive_get_extra_actions:
    """ 
        Router требует наличия метода get_extra_actions. Наследование от этого класса решает эту проблему 
    """
    @classmethod
    def get_extra_actions(cls):
        """ Фиктивный метод для прохождения проверки роутером """
        return []


class UserProfileView(RetrieveAPIView):
    """ 
        Просмотр пользователем своего профиля 
    """
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        language = JWT_DECODE_HANDLER(request.headers['Authorization'][7:])['language']
        try:
            user_profile = User.objects.get(phone_number=request.user.phone_number)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'name': user_profile.name,
                    'phone_number': user_profile.phone_number,
                    'level': user_profile.level,
                    'organization': user_profile.organization,
                    'language': language,
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)


class UserLoginView(APIView, Fictive_get_extra_actions):
    """ 
        Аутентификация пользователя, возвращающая токен 
    """
    queryset = ''
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)


class UserRegistrationView(CreateAPIView):
    """ Регистрация пользователя """
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            }
        
        return Response(response, status=status_code)


class NoteViewSet(viewsets.ModelViewSet):
    """ 
        Обработка обращений к модели Note 
    """
    permission_classes = (IsAuthenticated,) 
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
            organization_members = Note.objects.filter(organization=request.user.organization)
            organization_id = []
            for member in organization_members:
                organization_id.append(member.id)
            notes = Note.objects.filter(autor__in=request.organization_id)
        elif request.user.level == 'Admin':
            use_serializer = self.serializer_class
            notes = Note.objects.all()
        else:
            response = {
                    'success': 'false',
                    'status code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Note does not exists',
                    }
            return Response(response, status.HTTP_400_BAD_REQUEST)
        #Если всё прошло успешно
        serializer = use_serializer(instance=notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': f'Note {pk} does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    permission_classes = (IsAuthenticated,) 
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        note = self.get_object()
        return Response(note.highlighted)

    def perform_create(self, serializer):
        return super(UserViewSet, self).perform_create(serializer)


class OrganizationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = [JSONWebTokenAuthentication]
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        note = self.get_object()
        return Response(note.highlighted)

    def perform_create(self, serializer):
        return super(OrganizationViewSet, self).perform_create(serializer)
