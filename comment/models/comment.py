from django.db import models

from blog.models.blog import Post
from blogger import settings

class Comment(models.Model):
    """Model for comments"""
    
    body = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.body