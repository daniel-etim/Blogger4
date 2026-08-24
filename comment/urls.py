from django.urls import path

from comment.views.comment import create_comment, delete_comment

urlpatterns = [
    path("create/<int:pk>/", create_comment, name="create_comment"),
    path("delete/<int:pk>/", delete_comment, name="delete_comment"),
]