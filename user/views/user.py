import logging

from django.db import DatabaseError
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from user.serializers.user import RegisterUserSerializer, LoginUserSerializer, LogoutUserSerializer

# simple logger setup
logger = logging.getLogger(__name__)

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

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request: Request):
    """Get the refresh token, blacklist it, and return success msg when appropriate"""
    
    serializer = LogoutUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    clean_data = serializer.validated_data
    refresh_token_str = clean_data["refresh_token"]

    try:
        refresh_token= RefreshToken(refresh_token_str)
        refresh_token.blacklist()
        return Response(data={"message": "Logout successful"}, status=status.HTTP_200_OK)
    except TokenError:
        return Response(data={"error": "Invalid or Expired Token"}, status=status.HTTP_403_FORBIDDEN)
    except DatabaseError:
        logger.error(f"Failed to blacklist token {refresh_token_str[:10]}... due to DB error")
        return Response(
            data={
                "message": "Logged out (server sync delayed)",
                "action": "delete_local_tokens",
                "warning": "Token may remain valid until natural expiration"
            }, 
            status=status.HTTP_200_OK)