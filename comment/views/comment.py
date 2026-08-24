from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from blog.models.blog import Post
from comment.serializers.comment import CommentCreateSerializer


PND = "Post Not Found"

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_comment(request: Request, pk: int):
    """..."""

    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(data={"error": PND}, status = status.HTTP_404_NOT_FOUND)

    serializer = CommentCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer = serializer.save(author=request.user, post=post)

    serializer_data = {
        "post": str(serializer.post),
        "comment": serializer.body,
        "created_at": serializer.created_at,
        "author": str(serializer.author),
        "id": serializer.id
    }

    return Response(data=serializer_data, status=status.HTTP_201_CREATED)