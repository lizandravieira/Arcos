from django.contrib import admin
from django.urls import path
from app_arcos import views


urlpatterns = [
  path("", views.index, name="index"),
  path("login/", views.login, name="login"),
  path("register/",views.register, name="register"),
  path("admin/", admin.site.urls),
  path("plataforma",views.plataforma, name="plataforma"),
]
