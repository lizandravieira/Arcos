from django.contrib import admin
from django.urls import path
from app_arcos import views


urlpatterns = [
  path("", views.index, name="index"),

  path("login/", views.login, name="login"),
  path("register/",views.register, name="register"),
  path("logout/",views.logout, name="logout"),
  path("admin/", admin.site.urls),

  path("org/panel", views.org_panel_index, name="org_panel_index"),
  path("org/panel/contact", views.org_panel_contact, name="org_panel_contact"),

]
