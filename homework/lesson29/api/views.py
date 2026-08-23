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

from django.http import JsonResponse
from django.shortcuts import render
from .tasks import hello_world, multiply

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

    def retrieve(self, request, *args, **kwargs):
        product_id = kwargs["pk"]
        cache_key = f"product_detail_{product_id}"

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            print(f"PRODUCT {product_id} - CACHE HIT")
            return Response(cached_data)

        print(f"PRODUCT {product_id} - CACHE MISS")

        product = self.get_object()
        serializer = self.get_serializer(product)

        cache.set(cache_key, serializer.data, 60)

        return Response(serializer.data)

    def perform_update(self, serializer):
        product = serializer.save()

        cache_key = f"product_detail_{product.pk}"
        cache.delete(cache_key)

        print(f"USUNIĘTO CACHE DLA PRODUKTU {product.pk}")

def hello_world_view(request):
    hello_world.delay()

    return JsonResponse({
        "message": "Zadanie hello_world zostało wysłane do Celery."
    })


def multiply_view(request):
    message = None

    if request.method == "POST":
        a = int(request.POST.get("a"))
        b = int(request.POST.get("b"))

        task = multiply.delay(a, b)

        message = f"Zadanie wysłano do Celery. ID zadania: {task.id}"

    return render(
        request,
        "api/multiply_form.html",
        {"message": message},
    )
