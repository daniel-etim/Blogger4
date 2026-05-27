from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from user.serializers.user import RegisterUserSerializer



@api_view(["POST"])
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