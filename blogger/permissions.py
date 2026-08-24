from blog.models.blog import Post
from comment.models.comment import Comment

from user.models.user import User

def check_post_owner(post: Post, user: User) -> bool:
    """checks the authenticated user for the post"""

    return post.author == user

def check_comment_owner(comment: Comment, user: User) -> bool:
    """checks the authenticated user for the comment"""

    return comment.author == user