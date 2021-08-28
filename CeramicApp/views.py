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


class UserProfileView(RetrieveAPIView):

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

class UserLoginView(APIView):

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
    @classmethod
    def get_extra_actions(cls):
        """ Фиктивный метод для прохождения проверки роутером """
        return []

class UserRegistrationView(CreateAPIView):

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
    @classmethod
    def get_extra_actions(cls):
        """ Фиктивный метод для прохождения проверки роутером """
        return []

class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        note = self.get_object()
        return Response(note.highlighted)

    def perform_create(self, serializer):
        return super(NoteViewSet, self).perform_create(serializer)

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        note = self.get_object()
        return Response(note.highlighted)

    def perform_create(self, serializer):
        return super(UserViewSet, self).perform_create(serializer)

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        note = self.get_object()
        return Response(note.highlighted)

    def perform_create(self, serializer):
        return super(OrganizationViewSet, self).perform_create(serializer)
