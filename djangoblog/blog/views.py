from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import Post, Comment, Category


def index(request):
    posts = Post.objects.all().order_by("-created_at")
    
    category_id = request.GET.get("category")
    if category_id:
        posts = posts.filter(category_id=category_id)
    
    search_query = request.GET.get("search", "")
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )
    
    categories = Category.objects.all()
    selected_category = None
    if category_id:
        selected_category = get_object_or_404(Category, id=category_id)
    
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "posts/index.html",
        {
            "page_obj": page_obj,
            "search_query": search_query,
            "categories": categories,
            "selected_category": selected_category,
            "category_id": category_id,
        },
    )


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by("-created_at")
    if request.method == "POST":
        author = request.POST.get("author")
        text = request.POST.get("text")
        if author and text:
            Comment.objects.create(post=post, author=author, text=text)
            messages.success(request, "Комментарий добавлен успешно!")
            return redirect("post_detail", post_id=post.id)
        else:
            messages.error(request, "Пожалуйста, заполните все поля.")
    return render(
        request, "posts/post_detail.html", {"post": post, "comments": comments}
    )


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        author = request.POST.get("author")
        text = request.POST.get("text")
        if author and text:
            Comment.objects.create(post=post, author=author, text=text)
            messages.success(request, "Комментарий добавлен успешно!")
            return redirect("post_detail", post_id=post.id)
        else:
            messages.error(request, "Пожалуйста, заполните все поля.")
    return render(request, "posts/add_comment.html", {"post": post})



