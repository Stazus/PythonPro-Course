from datetime import date

from django.contrib import admin
from django.utils.html import format_html
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "availability_status", "car_age", "photo_thumbnail")
    search_fields = ("brand", "model")
    list_filter = ("year", "is_available")
    ordering = ("-year",)
    actions = ("mark_as_available",)

    @admin.display(description="Wiek samochodu")
    def car_age(self, obj):
        return date.today().year - obj.year

    @admin.display(description="Dostępność")
    def availability_status(self, obj):
        if obj.is_available:
            return format_html('<span style="color: green;">Dostępny</span>')
        return format_html('<span style="color: red;">Niedostępny</span>')

    @admin.display(description="Zdjęcie")
    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="100" height="60" style="object-fit: cover;">',
                obj.photo.url,
            )
        return "Brak zdjęcia"

    @admin.action(description="Oznacz wybrane samochody jako dostępne")
    def mark_as_available(self, request, queryset):
        queryset.update(is_available=True)
