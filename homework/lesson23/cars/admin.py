from django.contrib import admin
from django.utils.html import format_html
from .models import Car, Dealer

class CarInline(admin.TabularInline):
    model = Car
    extra = 0

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    inlines = [CarInline]

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "is_available", "photo_thumbnail", "full_name")
    search_fields = ("brand", "model")
    list_filter = ("year", "is_available")
    ordering = ("-year",)
    readonly_fields = ("year",)
    actions = ("mark_as_unavailable",)


    def full_name(self, obj):
        return f"{obj.brand} {obj.model}"

    full_name.short_description = "Pełna nazwa"

    @admin.display(description="Zdjęcie")
    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="150" height="60" style="object-fit: cover;">',
                obj.photo.url,
            )
        return "Brak zdjęcia"

    @admin.action(description="Oznacz jako niedostępne")
    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(
            request,
            f"Oznaczono jako niedostępne: {updated}",
        )
