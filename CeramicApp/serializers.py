from rest_framework import serializers, authentication
from CeramicApp.models import AccessLevel, Organization, Language, Session, Note, User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
import jwt
from django.conf import settings

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Creates a new user.
    phone_number, name, and password are required.
    Returns a JSON web token.
    """

    # The password must be validated and should not be read by the client
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('phone_number', 'name', 'password', 'token',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    """
    Authenticates an existing user.
    phone_number and password are required.
    Returns a JSON web token.
    """
    phone_number = serializers.CharField(max_length=11, write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    name = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """
        Validates user data.
        """
        phone_number = data.get('phone_number', None)
        password = data.get('password', None)

        if phone_number is None:
            raise serializers.ValidationError(
                'An phone_number is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=phone_number, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this phone_number and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'token': user.token.decode('utf-8'),
        }


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
