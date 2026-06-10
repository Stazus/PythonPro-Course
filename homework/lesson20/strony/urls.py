from django.urls import path
from . import views

urlpatterns = [
    path("info/", views.info),
    path("rules/", views.rules),
    path("user/<str:username>/", views.user_profile),
    path("products/", views.product_list),
    path("products/add/", views.add_product),
]
