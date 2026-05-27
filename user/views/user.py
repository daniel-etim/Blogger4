from django.contrib.auth import authenticate

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers.user import RegisterUserSerializer, LoginUserSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def user_register(request: Request):
    """Register a new user acct. Return 200 OK and user data upon success"""

    serializer = RegisterUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    data = {
        "message": "Registered successfully", 
        "username": user.username, 
        "email": user.email
    }

    return Response(data=data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request: Request):
    """Generate token, and return success message if user credentials are valid"""

    serializer = LoginUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    clean_data = serializer.validated_data
    user = authenticate(request, email=clean_data["email"], password=clean_data["password"])

    if not user:
        return Response(data={"error": "Incorrect email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token

    return Response(
        data={
            "message": "Login Successfully", 
            "username": user.username, 
            "refresh_token": str(refresh_token), "access_token" : str(access_token)
        }, 
        status=status.HTTP_200_OK)