from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django_mongodb_backend.fields import ObjectIdAutoField
from .models import User, Note

# Map ObjectIdAutoField to CharField so DRF handles MongoDB ObjectIds without int() casting errors
serializers.ModelSerializer.serializer_field_mapping[ObjectIdAutoField] = serializers.CharField


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer to handle user registration with password hashing.
    """
    id = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'interests']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


# Note Serializer
class NoteSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(source='user_id', read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'user', 'title', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class UserlistSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'interests']
        read_only_fields = ['id']
