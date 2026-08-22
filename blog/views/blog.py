from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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

    page_size = 5
    page_num = request.query_params.get("page", 1)

    paginator = Paginator(posts, page_size)

    try:
        paginated_posts = paginator.page(page_num)
    except PageNotAnInteger:
        page_num = 1
        paginated_posts = paginator.page(1)
    except EmptyPage:
        page_num = paginator.num_pages
        paginated_posts = paginator.page(paginator.num_pages)

    if not paginated_posts:
        return Response(data={"message": "No posts yet"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostListSerializer(paginated_posts, many=True)

    response_data = {
        "count": paginator.count,
        "total_pages": paginator.num_pages,
        "current_page": int(page_num),
        "previous_page": paginated_posts.has_previous(),
        "next_page": paginated_posts.has_next(),

        "data": serializer.data
    }

    return Response(data=response_data, status=status.HTTP_200_OK)

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