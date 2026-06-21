from django.contrib import admin
from .models import Note, Category, Article, Post, Tag

admin.site.register(Note)
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Post)
admin.site.register(Tag)
