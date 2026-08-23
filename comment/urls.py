from django.urls import path

from comment.views.comment import create_comment

urlpatterns = [
    path("create/", create_comment, name="create_comment"),
]