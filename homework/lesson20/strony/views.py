from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm



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

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/products/")
    else:
        form = ProductForm()


    return render(request, "add_product.html", {"form": form})
