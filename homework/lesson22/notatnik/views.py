from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Note, Category, Article, Post


def note_list(request):
    notes = Note.objects.all()

    paginator = Paginator(notes, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "note_list.html",
        {"page_obj": page_obj}
    )


def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, "note_detail.html", {"note": note})

def category_list(request):
    categories = Category.objects.all()

    return render(
        request,
        "category_list.html",
        {"categories": categories}
    )
    
    
def category_detail_view(request, pk):
    category = get_object_or_404(Category, id=pk)

    return render(
        request,
        "category_detail.html",
        {"category": category}
    )
    
    
def article_list(request):
    q = request.GET.get("q")

    articles = Article.objects.filter(
        is_published=True
    )

    if q:
        articles = articles.filter(
            title__icontains=q
        )

    articles = articles.order_by("-created_at")

    return render(
        request,
        "article_list.html",
        {
            "articles": articles,
            "q": q,
        }
    )


def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    posts = Post.objects.filter(
        category=category
    )

    return render(
        request,
        "posts_by_category.html",
        {
            "category": category,
            "posts": posts,
        }
    )
    
def post_list(request):
    q = request.GET.get("q")

    posts = Post.objects.all()

    if q:
        posts = posts.filter(
            Q(title__icontains=q) | Q(content__icontains=q)
        )

    posts = posts.order_by("-created_at")[:5]

    return render(
        request,
        "post_list.html",
        {
            "posts": posts,
            "q": q,
        }
    )
    
    
    
    
