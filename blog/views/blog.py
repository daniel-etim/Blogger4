from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from blog.serializers.blog import PostListSerializer, PostCreateSerializer, PostUpdateSerializer
from blog.models.blog import Post


@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list(request: Request):
    """Return list of posts, with 200 OK"""
    
    posts = Post.objects.all()
    serializer = PostListSerializer(posts, many=True)

    return Response(data={"post_list": serializer.data}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_create(request: Request):
    """Create and return post data"""
    serializer = PostCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.save(author=request.user)

    return Response(data={"post": serializer.data}, status=status.HTTP_201_CREATED)

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def post_update(request: Request, pk: int):
    """Update and return post data with 200 OK upon success"""
    
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(data={"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if post.author != request.user:
        return Response(data={"error": "You're not authorized to edit this post."}, status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = PostUpdateSerializer(post, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)

    serializer.save()
     
    return Response(data={"message": "Successfully updated", "post": serializer.data}, status=status.HTTP_200_OK)