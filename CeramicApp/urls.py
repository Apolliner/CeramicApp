from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from CeramicApp import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'note', views.NoteViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'organization', views.OrganizationViewSet)
router.register(r'registration', views.RegistrationAPIView, basename='user_registration')
router.register(r'login', views.LoginAPIView, basename='user_login')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^registration/?$', views.RegistrationAPIView.as_view(), name='user_registration'),
    re_path(r'^login/?$', views.LoginAPIView.as_view(), name='user_login'),

]