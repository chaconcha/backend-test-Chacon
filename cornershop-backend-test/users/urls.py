from django.urls import path

from . import views

urlpatterns = [
    path("/", views.loginView, name="login"),
    path("/auth/", views.auth_login, name="auth-login"),
]
