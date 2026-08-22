from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Note, Product
from .serializers import NoteSerializer, ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


@api_view(["GET"])
def set_name(request):
    name = request.query_params.get("name", "Gość")
    response = Response({"message": f"Ustawiono imię: {name}"})
    response.set_cookie("user_name", name)
    return response


@api_view(["GET"])
def hello(request):
    name = request.COOKIES.get("user_name", "Gość")
    return Response({"message": f"Witaj, {name}!"})


@api_view(["GET"])
def calculate(request):
    num1 = request.query_params.get("num1")
    num2 = request.query_params.get("num2")
    operation = request.query_params.get("operation")

    try:
        num1 = float(num1)
        num2 = float(num2)
    except (TypeError, ValueError):
        return Response(
            {"error": "Parametry num1 i num2 muszą być liczbami."},
            status=400,
        )

    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
            return Response(
                {"error": "Nie można dzielić przez zero."},
                status=400,
            )
        result = num1 / num2
    else:
        return Response(
            {"error": "Nieprawidłowa operacja."},
            status=400,
        )

    return Response({"result": result})
