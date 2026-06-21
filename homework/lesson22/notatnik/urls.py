from django.urls import path
from . import views

urlpatterns = [
    path("", views.note_list),
    path("note/<int:note_id>/", views.note_detail),
    path("categories/", views.category_list, name="category_list"),
    path("articles/", views.article_list, name="article_list"),
]

