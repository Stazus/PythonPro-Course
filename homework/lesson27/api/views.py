from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import time

from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60))
    def get(self, request):
        print("WYKONANO WIDOK - CACHE MISS")
        return Response({
            "username": request.user.username
        })



class SelectiveCacheView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        User = get_user_model()

        # Proste i szybkie zapytanie do bazy - wykonuje się za każdym razem
        users_count = User.objects.count()
        print("WYKONANO ZAPYTANIE DO BAZY")

        # Cachujemy tylko wynik kosztownego obliczenia
        cache_key = "complex_calculation_result"
        complex_result = cache.get(cache_key)

        if complex_result is None:
            print("CACHE MISS - wykonuję skomplikowane obliczenia")
            time.sleep(3)
            complex_result = 42
            cache.set(cache_key, complex_result, 60)
        else:
            print("CACHE HIT - wynik skomplikowanych obliczeń z cache")

        return Response({
            "users_count": users_count,
            "complex_result": complex_result,
        })


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @method_decorator(cache_page(60 * 10))
    def list(self, request, *args, **kwargs):
        print("PRODUCT LIST - wykonano widok")
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60))
    def retrieve(self, request, *args, **kwargs):
        print("PRODUCT RETRIEVE - wykonano widok")
        return super().retrieve(request, *args, **kwargs)
