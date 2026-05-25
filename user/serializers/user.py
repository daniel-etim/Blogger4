from rest_framework import serializers

from models.user import User


class RegisterUserSerializer(serializers.ModelSerializer):
    """A ModelSerializer. Accepts register info, with username, email, and password as obligatory"""
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]