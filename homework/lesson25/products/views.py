from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


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
