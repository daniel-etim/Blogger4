from django.urls import path

from comment.views.comment import create_comment

urlpatterns = [
    path("create/<int:pk>/", create_comment, name="create_comment"),
]