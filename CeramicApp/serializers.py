from rest_framework import serializers
from CeramicApp.models import AccessLevel, Organization, Language, Session, Note, User
from django.contrib.auth.hashers import make_password

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
