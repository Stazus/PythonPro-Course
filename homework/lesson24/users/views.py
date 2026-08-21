from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Konto dla {user.username} zostało utworzone!",
            )
            return redirect("home")

    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def home(request):
    return render(request, "home.html")


@staff_member_required
def user_list(request):
    users = User.objects.all()
    return render(request, "user_list.html", {"users": users})
