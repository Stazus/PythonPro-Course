from django.contrib import admin
from .models import Ogloszenie


@admin.register(Ogloszenie)
class OgloszenieAdmin(admin.ModelAdmin):
    list_display = ("tytul", "cena", "data_dodania")
