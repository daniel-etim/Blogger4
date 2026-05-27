from django.views.decorators.http import require_GET
from rest_framework import serializers

from user.models.user import User

 

class RegisterUserSerializer(serializers.ModelSerializer):
    """ModelSerializer for user registratiion. 
    
    It uses the custom `create` method. There the password is hashed when creating a new user
    """

    password = serializers.CharField(write_only=True, max_length=128, required=True, min_length=8)
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

    def create(self, validated_data):
        """create(with the password hashed) and return a new user object.
        
        We define this custom method as the parent `create` method don't hash password
        """
        
        return User.objects.create_user(
            first_name=validated_data.get("first_name", "",),
            last_name=validated_data.get("last_name", ""),
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
    

class LoginUserSerializer(serializers.Serializer):
    """Serializer for user login.
    - email
    - password
    """
    
    email = serializers.EmailField()
    password = serializers.CharField(required=True, write_only=True, max_length=128,  min_length=8)


class LogoutUserSerializer(serializers.Serializer):
    """Serializer for user Logout.
    - refresh_token"""
    refresh_token = serializers.CharField(required=True)