from rest_framework import serializers, authentication
from CeramicApp.models import AccessLevel, Organization, Language, Session, Note, User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
JWT_DECODE_HANDLER = api_settings.JWT_DECODE_HANDLER

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'

class UserLoginSerializer(serializers.Serializer):

    phone_number = serializers.CharField(max_length=11, min_length=11)
    password = serializers.CharField(max_length=128, write_only=True)
    language = serializers.CharField(max_length=2, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        phone_number = data.get("phone_number", None)
        password = data.get("password", None)
        language = data.get("language", None)
        user = authenticate(phone_number=phone_number, password=password)
        
        if user is None:
            raise serializers.ValidationError('A user with this phone number and password is not found.')
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            payload['language'] = language
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'phone_number':user.phone_number,
            'token': jwt_token
        }

class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name', 'phone_number', 'password', 'organization')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор общедоступной информации о пользователях """
    class Meta:
        model = User
        exclude = ("is_superuser", "groups", "user_permissions")
        depth = 1


class ProfileSerializer(serializers.ModelSerializer):
    """ Сериализатор личного профиля пользователя """
    class Meta:
        model = User
        exclude = ("is_superuser", "groups", "user_permissions")
        depth = 1


class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = '__all__'


class NoteSerializer(serializers.ModelSerializer):
    autor = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Note
        exclude = ['header', 'text']
        read_only_fields = ['id', 'autor', 'startdate']
        extra_kwargs = {
                        'header': {'source': 'header_en'},
                        'text': {'source': 'text_en'}
                        }


class UpdateUserSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    name = serializers.CharField(max_length=128, required=False)
    phone_number = serializers.CharField(max_length=11, min_length=11, required=False)
    password = serializers.CharField(max_length=128, required=False)
    level = serializers.CharField(max_length=128, required=False)
    organization = serializers.CharField(max_length=128, required=False)

