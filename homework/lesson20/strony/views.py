from django.http import HttpResponse


def info(request):
    return HttpResponse("To jest strona informacyjna.")


def rules(request):
    return HttpResponse("To jest regulamin serwisu.")

def user_profile(request, username):
    return HttpResponse(f"Witaj na profilu, {username}!")
