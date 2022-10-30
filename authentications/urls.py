"""URLs"""
from django.urls import path
from . import views
app_name = "authentications"
urlpatterns = [
    path("register/", views.register, name = "register"),
    path("login/", views.user_login, name = "login"),
    path("logout/", views.user_logout, name = "logout"),
    path("forget-password/", views.user_forgot_password, name = "forget_password"),
    path("forget-password-confirm/", views.user_forgot_pass_confirm, name = "forget_password_confirm")

]
