from rest_framework import renderers, viewsets, permissions, generics
from CeramicApp.models import AccessLevel, User, Organization, Language, Session, Note
from CeramicApp.serializers import UserSerializer, OrganizationSerializer, LanguageSerializer, SessionSerializer, NoteSerializer 
from CeramicApp.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view, action
from rest_framework.reverse import reverse
from rest_framework.response import Response


class NoteViewSet(viewsets.ModelViewSet):
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
