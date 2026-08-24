"""
URL configuration for mojastrona project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    ProtectedView,
    SelectiveCacheView,
    ProductViewSet,
    hello_world_view,
    multiply_view,
    process_video_view,
)


router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/protected/', ProtectedView.as_view(), name='protected'),
    path("__debug__/", include("debug_toolbar.urls")),
    path(
        'api/selective-cache/',
        SelectiveCacheView.as_view(),
        name='selective-cache'
),
    path('api/', include(router.urls)),
    path(
        "api/hello-celery/",
        hello_world_view,
        name="hello-celery",
    ),
    path(
        "api/multiply/",
        multiply_view,
        name="multiply",
    ),
    path(
        "api/process-video/",
        process_video_view,
        name="process-video",
    ),
]
