from django.urls import path

from user.views.user import user_register



urlpatterns = [
    path("register/", user_register, name="user_register"),
]