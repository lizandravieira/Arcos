from django.contrib import admin
from django.urls import path
from app_arcos import views
from django.conf import settings  # new
from django.urls import path, include  # new
from django.conf.urls.static import static  # new


urlpatterns = [
  path("", views.index, name="index"),
  path("login/", views.login, name="login"),
  path("register/",views.register, name="register"),
  path("logout/",views.logout, name="logout"),
  path("admin/", admin.site.urls),

  path("org/panel", views.org_panel_index, name="org_panel_index"),
  path("org/panel/contact", views.org_panel_contact, name="org_panel_contact"),
  path("org/panel/settings", views.org_panel_settings, name="org_panel_settings"),
  path("org/panel/settings/update",views.org_panel_update_settings, name='org_panel_update_settings'),


  path("org/panel/actions", views.org_panel_actions_index, name="org_panel_actions_index"),
  path("org/panel/actions/create", views.org_panel_actions_create, name="org_panel_actions_create"),
  path("org/panel/actions/<int:id>/delete", views.org_panel_actions_delete, name="org_panel_actions_delete"),

  path("org/panel/donations/index", views.org_panel_donations_index, name="org_panel_donations_index"),
  path("org/panel/donations/list", views.org_panel_donations_list, name="org_panel_donations_list"),
  path("org/panel/donations/<int:id>/confirm", views.org_panel_donations_confirm, name="org_panel_donations_confirm"),


  path("view/site/<str:username>", views.view_site, name="view_site"),
  path("view/site/<str:username>/actions", views.view_site_actions, name="view_site_actions"),
  path("view/site/<str:username>/actions/<int:id>", views.view_site_action, name="view_site_action"),
  path("view/site/<str:username>/contact", views.view_site_contact, name="view_site_contact"),
  path("view/site/<str:username>/donate", views.view_site_donate, name="view_site_donate"),
  path("view/site/<str:username>/donations", views.view_site_donations, name="view_site_donations"),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

