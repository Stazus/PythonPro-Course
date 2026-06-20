from django.urls import path
from . import views

urlpatterns = [
    path("", views.note_list),
    path("note/<int:note_id>/", views.note_detail),
]
