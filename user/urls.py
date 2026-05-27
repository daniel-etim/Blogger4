from django.urls import path

from user.views.user import user_register, user_login



urlpatterns = [
    path("register/", user_register, name="user_register"),
    path("login/", user_login, name="user_login"),
]