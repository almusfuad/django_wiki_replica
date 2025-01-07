from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search", views.searching, name='search'),
    path("wiki/create_new_wiki", views.create_new_page, name="create_new_wiki"),
    path("wiki/<str:entry>", views.entry_page, name="entry_page"),
    path("wiki/edit/<str:entry>", views.edit_page, name="edit_page"),
]
