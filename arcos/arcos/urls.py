
from django.urls import path
from app_arcos import views


urlpatterns = [
  path("", views.index, name="index"),
  path("login/", views.login, name="login"),
  # path("logout/", views.logout_view, name="logout"),
  # path("register/", views.register, name="register"),
]
