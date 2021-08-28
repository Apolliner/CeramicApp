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

#class LoginAPIView(APIView):

#    permission_classes = [AllowAny]
#    serializer_class = LoginSerializer

#    def post(self, request):

#        serializer = self.serializer_class(data=request.data)
#        serializer.is_valid(raise_exception=True)

#        return Response(serializer.data, status=status.HTTP_200_OK)
#    @classmethod
#    def get_extra_actions(cls):
#        """ Фиктивный метод для прохождения проверки роутером """
#        return []

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

#class RegistrationAPIView(APIView):
#    """
#    Registers a new user.
#    """
#    permission_classes = [IsOwnerOrReadOnly]#[AllowAny]
#    serializer_class = RegistrationSerializer

#    def post(self, request):
#        """
#        Creates a new User object.
#        Username, phone_number, and password are required.
#        Returns a JSON web token.
#        """
#        serializer = self.serializer_class(data=request.data)
#        serializer.is_valid(raise_exception=True)
#        serializer.save()

#        return Response(
#            {
#                'token': serializer.data.get('token', None),
#            },
#            status=status.HTTP_201_CREATED,
#        )
#    @classmethod
#    def get_extra_actions(cls):
#        """ Фиктивный метод для прохождения проверки роутером """
#        return []

#class LoginAPIView(APIView):
#    """
#    Logs in an existing user.
#    """
#    permission_classes = [AllowAny]
    #permission_classes = (IsAuthenticated,) 
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = [IsOwnerOrReadOnly]#[AllowAny]
#    serializer_class = LoginSerializer

#    def post(self, request):
#        """
#        Checks is user exists.
#        phone_number and password are required.
#        Returns a JSON web token.
#        """
#        serializer = self.serializer_class(data=request.data)
#        serializer.is_valid(raise_exception=True)

#        return Response(serializer.data, status=status.HTTP_200_OK)
#    @classmethod
#    def get_extra_actions(cls):
#        """ Фиктивный метод для прохождения проверки роутером """
#        return []


class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,) 
    authentication_classes = (TokenAuthentication,)
    #permission_classes = [IsOwnerOrReadOnly]
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
    #permission_classes = [IsOwnerOrReadOnly]
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
