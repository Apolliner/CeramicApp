from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from CeramicApp import views
from django.conf.urls import url

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'note', views.NoteViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'organization', views.OrganizationViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^registration/?$', views.UserRegistrationView.as_view(), name='user_registration'),
    re_path(r'^login/?$', views.UserLoginView.as_view(), name='user_login'),
    url(r'^profile', views.UserProfileView.as_view()),
    #re_path(r'note', views.NoteViewSet.as_view(), name='note')
]