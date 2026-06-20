from django.contrib import admin
from .models import Note, Category, Article

admin.site.register(Note)
admin.site.register(Category)
admin.site.register(Article)