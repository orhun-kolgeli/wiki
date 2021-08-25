from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("edit/", views.edit, name="edit"),
    path("random/", views.random, name="random"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("<str:title>/", views.titles, name="titles")
]
