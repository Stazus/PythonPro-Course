from datetime import date

from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "is_available", "car_age")
    search_fields = ("brand", "model")
    list_filter = ("year", "is_available")
    ordering = ("-year", "brand")

    @admin.display(description="Wiek samochodu")
    def car_age(self, obj):
        return date.today().year - obj.year
