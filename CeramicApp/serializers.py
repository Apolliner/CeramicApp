from rest_framework import serializers, authentication
from CeramicApp.models import AccessLevel, Organization, Language, Session, Note, User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
import jwt
from django.conf import settings
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.Serializer):

    phone_number = serializers.CharField(max_length=11)
    password = serializers.CharField(max_length=128, write_only=True)
    #language = serializers.CharField(max_length=2)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        phone_number = data.get("phone number", None)
        password = data.get("password", None)
        #language = data.get("language", 'en')
        user = authenticate(phone_number=phone_number, password=password)
        
        if user is None:
            raise serializers.ValidationError(
                'A user with this phone number and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
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
        fields = ('name', 'phone_number', 'password', 'level', 'organization')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
    #def create(self, validated_data):
    #    """
    #    Create and return a new `User` instance, given the validated data.
    #    """
    #    validated_data['password'] = make_password(validated_data['password'])
    #    return User.objects.create(**validated_data)


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'

class LanguageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Session
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Note
        #fields = ['autor', 'header', 'text', 'startdate']
        fields = '__all__'
    def create(self, validated_data):
        """
        Create and return a new `Note` instance, given the validated data.
        """
        return Note.objects.create(**validated_data)
