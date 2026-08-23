from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

@api_view(["POST"])
def create_comment(request: Request):
    """success message"""
    return Response(data={"message": "successful"}, status=status.HTTP_200_OK)