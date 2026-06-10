from django.urls import path
from . import views

urlpatterns = [
    path("info/", views.info),
    path("rules/", views.rules),
    path("user/<str:username>/", views.user_profile),
]
