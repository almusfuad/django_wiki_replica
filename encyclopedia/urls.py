from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry_page, name="entry_page"),
    path("wiki/edit/<str:entry>", views.edit_page, name="edit_page"),
]
