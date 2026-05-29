from django.utils.text import slugify

from rest_framework import serializers

from blog.models.blog import Post


class PostListSerializer(serializers.ModelSerializer):
    """ModelSerializer for post list.
    
    fields and read_only_fields are:
    - title
    - created_at
    - author
    """

    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ["title", "created_at", "author"]

        read_only_fields = ["title", "created_at", "author"]

class PostCreateSerializer(serializers.ModelSerializer):
    """ModelSerializer for post create"""

    author = serializers.StringRelatedField()

    # if user don't provide slug, we auto-generate from title
    slug = serializers.SlugField(required = False)
    
    class Meta:
        model = Post
        fields = ["title", "content", "slug", "created_at", "author"]

        read_only_fields = ["created_at", "author"]

    def create(self, validated_data):
        """We call this custom `create` method so that we can handle missing or not-unique slugs"""
        slug_title = slugify(validated_data["title"])
        slug = validated_data.get("slug", slug_title)

        base_slug = slug
        counter = 2

        while Post.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        validated_data["slug"] = slug

        return Post.objects.create(**validated_data)