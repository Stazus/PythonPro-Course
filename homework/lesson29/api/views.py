from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from celery import chain

import time

from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework import viewsets

from .models import Product, UploadedImage
from .serializers import ProductSerializer

from django.http import JsonResponse
from django.shortcuts import render
from .tasks import (
    hello_world,
    multiply,
    process_video,
    progress_task,
    generate_users_csv,
    classify_uploaded_image,
    generate_random_number,
    multiply_by_ten,
    save_chain_result,
)

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


def process_video_view(request):
    process_video.delay()

    return JsonResponse({
        "message": "Przetwarzanie wideo rozpoczęte!"
    })


from celery.result import AsyncResult


def start_progress_task_view(request):
    task = progress_task.delay()

    return JsonResponse({
        "task_id": task.id,
        "message": "Zadanie rozpoczęte.",
    })


def task_status_view(request, task_id):
    result = AsyncResult(task_id)

    response = {
        "task_id": task_id,
        "state": result.state,
    }

    if result.state == "PROGRESS":
        response["current"] = result.info.get("current", 0)
        response["total"] = result.info.get("total", 100)

    elif result.state == "SUCCESS":
        response["current"] = 100
        response["total"] = 100
        response["result"] = result.result

    return JsonResponse(response)


def start_users_csv_report_view(request):
    task = generate_users_csv.delay()

    return JsonResponse({
        "task_id": task.id,
        "message": "Generowanie raportu CSV rozpoczęte.",
    })


def users_csv_report_status_view(request, task_id):
    result = AsyncResult(task_id)

    response = {
        "task_id": task_id,
        "state": result.state,
    }

    if result.state == "SUCCESS":
        response["download_url"] = f"/media/{result.result}"

    return JsonResponse(response)


def upload_image_view(request):
    if request.method == "POST":
        image_file = request.FILES.get("image")

        if not image_file:
            return JsonResponse(
                {"error": "Nie przesłano obrazu."},
                status=400,
            )

        uploaded_image = UploadedImage.objects.create(
            image=image_file
        )

        task = classify_uploaded_image.delay(uploaded_image.id)

        return JsonResponse({
            "image_id": uploaded_image.id,
            "task_id": task.id,
            "message": "Obraz zapisano i przekazano do klasyfikacji.",
        })

    return render(request, "api/upload_image.html")


def start_chain_view(request):
    task_chain = chain(
        generate_random_number.s(),
        multiply_by_ten.s(),
        save_chain_result.s(),
    )

    result = task_chain.apply_async()

    return JsonResponse({
        "task_id": result.id,
        "message": "Łańcuch zadań został uruchomiony.",
    })
