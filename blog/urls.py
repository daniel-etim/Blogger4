from django.urls import path

from blog.views.blog import post_list, post_read, post_create, post_update, post_delete


urlpatterns = [
    path("", post_list, name="post_list"),
    path("read/<int:pk>/", post_read, name="post_read"),
    path("create/", post_create, name="post_create"),
    path("update/<int:pk>/", post_update, name="post_update"),
    path("delete/<int:pk>/", post_delete, name="post_delete"),
]