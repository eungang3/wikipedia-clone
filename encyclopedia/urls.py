from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("get_random/", views.get_random, name="get_random"),
    path("edit/<str:title>", views.edit, name="edit")
]
