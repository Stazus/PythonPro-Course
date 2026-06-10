from django.shortcuts import render
from .models import Product

from django.http import HttpResponse


def info(request):
    return HttpResponse("To jest strona informacyjna.")


def rules(request):
    return HttpResponse("To jest regulamin serwisu.")

def user_profile(request, username):
    return HttpResponse(f"Witaj na profilu, {username}!")
def product_list(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})
