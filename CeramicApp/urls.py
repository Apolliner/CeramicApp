from django.urls import path, include
from rest_framework.routers import DefaultRouter
from CeramicApp import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'note', views.NoteViewSet)
router.register(r'user', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]