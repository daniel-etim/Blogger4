from user.models.user import User
from blog.models.blog import Post

def check_post_owner(post: Post, user: User) -> bool:
    """checks the authenticated user for the post"""

    return post.author == user