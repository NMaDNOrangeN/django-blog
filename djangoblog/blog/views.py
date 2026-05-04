from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Post, Comment


def index(request):
    posts = Post.objects.all().order_by("-created_at")
    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "posts/index.html", {"page_obj": page_obj})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by("-created_at")
    if request.method == "POST":
        author = request.POST.get("author")
        text = request.POST.get("text")
        if author and text:
            Comment.objects.create(post=post, author=author, text=text)
            messages.success(request, "Comment added successfully!")
            return redirect("post_detail", post_id=post.id)
        else:
            messages.error(request, "Please fill in all fields.")
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
            messages.success(request, "Comment added successfully!")
            return redirect("post_detail", post_id=post.id)
        else:
            messages.error(request, "Please fill in all fields.")
    return render(request, "posts/add_comment.html", {"post": post})


def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        author = request.POST.get("author")
        text = request.POST.get("text")
        if author and text:
            comment.author = author
            comment.text = text
            comment.save()
            messages.success(request, "Comment updated successfully!")
            return redirect("post_detail", post_id=comment.post.id)
        else:
            messages.error(request, "Please fill in all fields.")
    return render(request, "posts/edit_comment.html", {"comment": comment})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
        return redirect("post_detail", post_id=comment.post.id)
    return render(request, "posts/delete_comment.html", {"comment": comment})
