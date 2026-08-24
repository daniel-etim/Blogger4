from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from comment.models.comment import Comment

class CommentCreateSerializer(serializers.ModelSerializer):
    """ModelSerializer..."""

    author = StringRelatedField()
    post = StringRelatedField()

    class Meta:
        model = Comment
        fields = ["post", "body", "created_at", "author", "id"]

        read_only_fields = ["post", "created_at", "author", "id"]